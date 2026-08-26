locals {
  action_names = toset(keys(var.role_arns))
}

data "archive_file" "lambda" {
  for_each    = local.action_names
  type        = "zip"
  output_path = "${path.module}/${each.key}.zip"

  source {
    content  = file("${var.source_root}/lambda/${each.key}/app.py")
    filename = "app.py"
  }

  dynamic "source" {
    for_each = fileset("${var.source_root}/shared/aws_ir", "*.py")
    content {
      content  = file("${var.source_root}/shared/aws_ir/${source.value}")
      filename = "aws_ir/${source.value}"
    }
  }
}

resource "aws_lambda_function" "action" {
  for_each         = local.action_names
  function_name    = "${var.project_name}-${replace(each.key, "_", "-")}"
  role             = var.role_arns[each.key]
  handler          = "app.handler"
  runtime          = "python3.13"
  filename         = data.archive_file.lambda[each.key].output_path
  source_code_hash = data.archive_file.lambda[each.key].output_base64sha256
  timeout          = var.timeout_seconds
  memory_size      = var.memory_mb

  environment {
    variables = { INCIDENT_TOPIC_ARN = var.incident_topic_arn }
  }

  tags = var.tags
}
