output "function_names" {
  value = { for key, value in aws_lambda_function.action : key => value.function_name }
}

output "incident_topic_arn" {
  value = aws_sns_topic.incident.arn
}

output "kms_key_arn" {
  value = aws_kms_key.sns.arn
}
