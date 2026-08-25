data "archive_file" "detection_normalizer" {
  type        = "zip"
  output_path = "${path.module}/normalize_security_event.zip"

  source {
    content  = file("${path.module}/../detection/normalizer/app.py")
    filename = "app.py"
  }
}

resource "aws_sqs_queue" "detection_dlq" {
  name                      = "${var.project_name}-detection-dlq"
  message_retention_seconds = var.detection_dlq_retention_seconds
  kms_master_key_id         = "alias/aws/sqs"
  tags                      = local.common_tags
}

resource "aws_dynamodb_table" "detection_dedup" {
  name         = "${var.project_name}-detection-dedup"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "dedupe_key"

  attribute {
    name = "dedupe_key"
    type = "S"
  }

  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "detection_normalizer" {
  name              = "/aws/lambda/${var.project_name}-normalize-security-event"
  retention_in_days = var.log_retention_days
  tags              = local.common_tags
}

resource "aws_iam_role" "detection_normalizer" {
  name = "${var.project_name}-detection-normalizer-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
  tags = local.common_tags
}

resource "aws_iam_role_policy" "detection_normalizer" {
  name = "${var.project_name}-detection-normalizer-policy"
  role = aws_iam_role.detection_normalizer.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "Logs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "${aws_cloudwatch_log_group.detection_normalizer.arn}:*"
      },
      {
        Sid      = "AcquireDeduplicationKey"
        Effect   = "Allow"
        Action   = ["dynamodb:PutItem"]
        Resource = aws_dynamodb_table.detection_dedup.arn
      },
      {
        Sid      = "StartReadOnlyTriage"
        Effect   = "Allow"
        Action   = ["states:StartExecution"]
        Resource = aws_sfn_state_machine.ec2_incident_response.arn
      },
      {
        Sid      = "PublishNotifyOnly"
        Effect   = "Allow"
        Action   = ["sns:Publish"]
        Resource = aws_sns_topic.incident.arn
      },
      {
        Sid      = "UseIncidentTopicKey"
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:GenerateDataKey"]
        Resource = aws_kms_key.sns.arn
      }
    ]
  })
}

resource "aws_lambda_function" "detection_normalizer" {
  function_name    = "${var.project_name}-normalize-security-event"
  role             = aws_iam_role.detection_normalizer.arn
  handler          = "app.handler"
  runtime          = "python3.13"
  filename         = data.archive_file.detection_normalizer.output_path
  source_code_hash = data.archive_file.detection_normalizer.output_base64sha256
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      DEDUP_TABLE_NAME              = aws_dynamodb_table.detection_dedup.name
      DEDUP_TTL_SECONDS             = tostring(var.detection_dedup_ttl_seconds)
      STATE_MACHINE_ARN             = aws_sfn_state_machine.ec2_incident_response.arn
      INCIDENT_TOPIC_ARN            = aws_sns_topic.incident.arn
      DEFAULT_RESPONSE_ROUTE        = var.detection_default_route
      ALLOWED_ACCOUNT_IDS           = join(",", var.detection_allowed_account_ids)
      IGNORE_PRINCIPAL_ARN_PREFIXES = join(",", var.detection_ignore_principal_arn_prefixes)
    }
  }

  depends_on = [aws_cloudwatch_log_group.detection_normalizer, aws_iam_role_policy.detection_normalizer]
  tags       = local.common_tags
}

locals {
  detection_rules = {
    guardduty   = "guardduty-medium-high.json"
    securityhub = "securityhub-findings.json"
    config      = "config-noncompliant.json"
    cloudwatch  = "cloudwatch-alarm.json"
    cloudtrail  = "cloudtrail-trail-tampering.json"
  }
}

resource "aws_cloudwatch_event_rule" "detection" {
  for_each      = local.detection_rules
  name          = "${var.project_name}-${each.key}-detection"
  description   = "AWS IR selected ${each.key} event routing"
  event_pattern = file("${path.module}/../detection/event-patterns/${each.value}")
  state         = each.key == "cloudwatch" && !var.enable_cloudwatch_alarm_routing ? "DISABLED" : "ENABLED"
  tags          = local.common_tags
}

resource "aws_lambda_permission" "eventbridge_detection" {
  for_each      = aws_cloudwatch_event_rule.detection
  statement_id  = "AllowExecutionFromEventBridge-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.detection_normalizer.function_name
  principal     = "events.amazonaws.com"
  source_arn    = each.value.arn
}

resource "aws_cloudwatch_event_target" "detection" {
  for_each = aws_cloudwatch_event_rule.detection
  rule     = each.value.name
  arn      = aws_lambda_function.detection_normalizer.arn

  dead_letter_config {
    arn = aws_sqs_queue.detection_dlq.arn
  }

  retry_policy {
    maximum_event_age_in_seconds = var.detection_max_event_age_seconds
    maximum_retry_attempts       = var.detection_max_retry_attempts
  }

  depends_on = [aws_lambda_permission.eventbridge_detection]
}

resource "aws_sqs_queue_policy" "detection_dlq" {
  queue_url = aws_sqs_queue.detection_dlq.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "AllowEventBridgeDeadLetterDelivery"
      Effect    = "Allow"
      Principal = { Service = "events.amazonaws.com" }
      Action    = "sqs:SendMessage"
      Resource  = aws_sqs_queue.detection_dlq.arn
      Condition = {
        ArnEquals = { "aws:SourceArn" = [for rule in aws_cloudwatch_event_rule.detection : rule.arn] }
      }
    }]
  })
}

resource "aws_cloudwatch_event_archive" "detection" {
  count            = var.enable_detection_event_archive ? 1 : 0
  name             = "${var.project_name}-security-events"
  event_source_arn = "arn:${data.aws_partition.current.partition}:events:${var.aws_region}:${data.aws_caller_identity.current.account_id}:event-bus/default"
  retention_days   = var.detection_archive_retention_days
  event_pattern = jsonencode({
    source = ["aws.guardduty", "aws.securityhub", "aws.config", "aws.cloudwatch", "aws.cloudtrail"]
  })
  description = "Optional archive for selected AWS IR detection source events"
}

resource "aws_cloudwatch_log_metric_filter" "security_signal" {
  count          = var.cloudwatch_security_log_group_name == null ? 0 : 1
  name           = "${var.project_name}-security-log-signal"
  log_group_name = var.cloudwatch_security_log_group_name
  pattern        = "AccessDenied"

  metric_transformation {
    name      = "SecurityLogSignalCount"
    namespace = "AWSIR/${var.project_name}"
    value     = "1"
  }
}

resource "aws_cloudwatch_metric_alarm" "security_signal" {
  count               = var.cloudwatch_security_log_group_name == null ? 0 : 1
  alarm_name          = "${var.project_name}-security-log-signal"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = "SecurityLogSignalCount"
  namespace           = "AWSIR/${var.project_name}"
  period              = 300
  statistic           = "Sum"
  threshold           = 1
  treat_missing_data  = "notBreaching"
  tags                = local.common_tags
}
