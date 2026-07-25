output "function_names" {
  value       = { for key, value in aws_lambda_function.action : key => value.function_name }
  description = "Deployed Lambda function names by response action."
}

output "function_arns" {
  value       = { for key, value in aws_lambda_function.action : key => value.arn }
  description = "Deployed Lambda function ARNs by response action."
}

output "incident_topic_arn" {
  value       = aws_sns_topic.incident.arn
  description = "KMS-encrypted SNS topic used by the notification action."
}

output "kms_key_arn" {
  value       = aws_kms_key.sns.arn
  description = "KMS key protecting the incident notification topic."
}

output "configured_s3_bucket_arns" {
  value       = local.s3_bucket_arns_effective
  description = "S3 bucket ARNs embedded in the response-action execution policies."
}

output "configured_iam_user_arns" {
  value       = local.iam_user_arns_effective
  description = "IAM user ARNs embedded in the access-key response-action policies."
}
