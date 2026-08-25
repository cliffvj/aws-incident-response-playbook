resource "aws_sns_topic" "approval" {
  name              = "${var.project_name}-approvals"
  kms_master_key_id = aws_kms_key.sns.arn
  tags              = local.common_tags
}

resource "aws_sns_topic_subscription" "approval_email" {
  count     = var.approval_email_endpoint == null ? 0 : 1
  topic_arn = aws_sns_topic.approval.arn
  protocol  = "email"
  endpoint  = var.approval_email_endpoint
}

resource "aws_dynamodb_table" "orchestration_executions" {
  name         = "${var.project_name}-orchestration-executions"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "event_id"

  attribute {
    name = "event_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "step_functions" {
  name              = "/aws/vendedlogs/states/${var.project_name}-ec2-incident-response"
  retention_in_days = var.log_retention_days
  tags              = local.common_tags
}

resource "aws_iam_role" "step_functions" {
  name = "${var.project_name}-step-functions-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "states.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy" "step_functions" {
  name = "${var.project_name}-step-functions-policy"
  role = aws_iam_role.step_functions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "InvokeResponseActions"
        Effect = "Allow"
        Action = ["lambda:InvokeFunction"]
        Resource = [
          aws_lambda_function.action["collect_ec2_metadata"].arn,
          aws_lambda_function.action["snapshot_ebs_volumes"].arn,
          aws_lambda_function.action["ensure_quarantine_security_group"].arn,
          aws_lambda_function.action["isolate_ec2_instance"].arn,
          aws_lambda_function.action["restore_ec2_security_groups"].arn,
          aws_lambda_function.action["notify_incident"].arn,
        ]
      },
      {
        Sid      = "PublishApprovalRequests"
        Effect   = "Allow"
        Action   = ["sns:Publish"]
        Resource = [aws_sns_topic.approval.arn]
      },
      {
        Sid      = "UseApprovalTopicKey"
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:GenerateDataKey*"]
        Resource = [aws_kms_key.sns.arn]
      },
      {
        Sid    = "MaintainExecutionCorrelation"
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
        ]
        Resource = [aws_dynamodb_table.orchestration_executions.arn]
      },
      {
        Sid    = "StepFunctionsLogDelivery"
        Effect = "Allow"
        Action = [
          "logs:CreateLogDelivery",
          "logs:GetLogDelivery",
          "logs:UpdateLogDelivery",
          "logs:DeleteLogDelivery",
          "logs:ListLogDeliveries",
          "logs:PutResourcePolicy",
          "logs:DescribeResourcePolicies",
          "logs:DescribeLogGroups",
        ]
        Resource = ["*"]
      },
    ]
  })
}

resource "aws_iam_policy" "step_functions_approver" {
  name        = "${var.project_name}-step-functions-approver"
  description = "Allows an explicitly authorized responder to resolve Step Functions callback task tokens. Not attached automatically."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "ResolveApprovalTaskTokens"
      Effect = "Allow"
      Action = [
        "states:SendTaskSuccess",
        "states:SendTaskFailure",
      ]
      Resource = "*"
    }]
  })

  tags = local.common_tags
}

locals {
  ec2_incident_response_definition = replace(templatefile("${path.module}/../step-functions/ec2-incident-response.asl.json", {
    partition                = data.aws_partition.current.partition
    collect_metadata_arn     = aws_lambda_function.action["collect_ec2_metadata"].arn
    snapshot_ebs_arn         = aws_lambda_function.action["snapshot_ebs_volumes"].arn
    ensure_quarantine_arn    = aws_lambda_function.action["ensure_quarantine_security_group"].arn
    isolate_ec2_arn          = aws_lambda_function.action["isolate_ec2_instance"].arn
    restore_ec2_arn          = aws_lambda_function.action["restore_ec2_security_groups"].arn
    notify_incident_arn      = aws_lambda_function.action["notify_incident"].arn
    approval_topic_arn       = aws_sns_topic.approval.arn
    execution_table_name     = aws_dynamodb_table.orchestration_executions.name
    approval_timeout_seconds = var.approval_timeout_seconds
  }), "\"__APPROVAL_TIMEOUT_SECONDS__\"", tostring(var.approval_timeout_seconds))
}

resource "aws_sfn_state_machine" "ec2_incident_response" {
  name     = "${var.project_name}-ec2-incident-response"
  role_arn = aws_iam_role.step_functions.arn
  type     = "STANDARD"

  definition = local.ec2_incident_response_definition

  logging_configuration {
    include_execution_data = var.step_functions_include_execution_data
    level                  = "ALL"
    log_destination        = "${aws_cloudwatch_log_group.step_functions.arn}:*"
  }

  depends_on = [aws_iam_role_policy.step_functions]
  tags       = local.common_tags
}
