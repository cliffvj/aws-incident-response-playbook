data "aws_caller_identity" "current" {}

data "archive_file" "lambda" {
  for_each    = local.functions
  type        = "zip"
  output_path = "${path.module}/${each.key}.zip"

  source {
    content  = file("${path.module}/../lambda/${each.key}/app.py")
    filename = "app.py"
  }

  dynamic "source" {
    for_each = fileset("${path.module}/../shared/aws_ir", "*.py")
    content {
      content  = file("${path.module}/../shared/aws_ir/${source.value}")
      filename = "aws_ir/${source.value}"
    }
  }
}

resource "aws_kms_key" "sns" {
  description             = "KMS key for ${var.project_name} incident notifications"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  tags                    = local.common_tags
}

resource "aws_kms_alias" "sns" {
  name          = "alias/${var.project_name}-sns"
  target_key_id = aws_kms_key.sns.key_id
}

resource "aws_sns_topic" "incident" {
  name              = "${var.project_name}-notifications"
  kms_master_key_id = aws_kms_key.sns.arn
  tags              = local.common_tags
}

resource "aws_iam_role" "lambda" {
  for_each = local.functions
  name     = "${var.project_name}-${replace(each.key, "_", "-")}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy" "lambda" {
  for_each = local.functions
  name     = "${var.project_name}-${replace(each.key, "_", "-")}-policy"
  role     = aws_iam_role.lambda[each.key].id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "Logs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.project_name}-*:*"
      },
      {
        Sid      = "ActionPermissions"
        Effect   = "Allow"
        Action   = each.value
        Resource = "*"
      }
    ]
  })
}

resource "aws_cloudwatch_log_group" "lambda" {
  for_each          = local.functions
  name              = "/aws/lambda/${var.project_name}-${replace(each.key, "_", "-")}"
  retention_in_days = var.log_retention_days
  tags              = local.common_tags
}

resource "aws_lambda_function" "action" {
  for_each         = local.functions
  function_name    = "${var.project_name}-${replace(each.key, "_", "-")}"
  role             = aws_iam_role.lambda[each.key].arn
  handler          = "app.handler"
  runtime          = "python3.13"
  filename         = data.archive_file.lambda[each.key].output_path
  source_code_hash = data.archive_file.lambda[each.key].output_base64sha256
  timeout          = 60
  memory_size      = 256

  environment {
    variables = {
      INCIDENT_TOPIC_ARN = aws_sns_topic.incident.arn
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda]
  tags       = local.common_tags
}
