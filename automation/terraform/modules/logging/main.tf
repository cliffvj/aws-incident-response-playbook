resource "aws_cloudwatch_log_group" "lambda" {
  for_each          = var.action_names
  name              = "/aws/lambda/${var.project_name}-${replace(each.key, "_", "-")}"
  retention_in_days = var.retention_in_days
  tags              = var.tags
}

resource "aws_cloudwatch_log_group" "step_functions" {
  name              = "/aws/vendedlogs/states/${var.project_name}-ec2-incident-response"
  retention_in_days = var.retention_in_days
  tags              = var.tags
}

resource "aws_cloudwatch_log_group" "detection_normalizer" {
  name              = "/aws/lambda/${var.project_name}-normalize-security-event"
  retention_in_days = var.retention_in_days
  tags              = var.tags
}
