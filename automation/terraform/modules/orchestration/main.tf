resource "aws_dynamodb_table" "executions" {
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

  tags = var.tags
}

locals {
  definition = replace(templatefile("${var.source_root}/step-functions/ec2-incident-response.asl.json", {
    partition                = var.partition
    collect_metadata_arn     = var.function_arns["collect_ec2_metadata"]
    snapshot_ebs_arn         = var.function_arns["snapshot_ebs_volumes"]
    ensure_quarantine_arn    = var.function_arns["ensure_quarantine_security_group"]
    isolate_ec2_arn          = var.function_arns["isolate_ec2_instance"]
    restore_ec2_arn          = var.function_arns["restore_ec2_security_groups"]
    notify_incident_arn      = var.function_arns["notify_incident"]
    approval_topic_arn       = var.approval_topic_arn
    execution_table_name     = aws_dynamodb_table.executions.name
    approval_timeout_seconds = var.approval_timeout_seconds
  }), "\"__APPROVAL_TIMEOUT_SECONDS__\"", tostring(var.approval_timeout_seconds))
}

resource "aws_sfn_state_machine" "ec2_incident_response" {
  name       = "${var.project_name}-ec2-incident-response"
  role_arn   = var.role_arn
  type       = "STANDARD"
  definition = local.definition

  logging_configuration {
    include_execution_data = var.include_execution_data
    level                  = "ALL"
    log_destination        = "${var.log_group_arn}:*"
  }

  tags = var.tags
}
