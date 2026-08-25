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

output "state_machine_arn" {
  value       = aws_sfn_state_machine.ec2_incident_response.arn
  description = "Reference EC2 incident-response Step Functions state machine ARN."
}

output "state_machine_name" {
  value       = aws_sfn_state_machine.ec2_incident_response.name
  description = "Reference EC2 incident-response Step Functions state machine name."
}

output "approval_topic_arn" {
  value       = aws_sns_topic.approval.arn
  description = "Dedicated KMS-encrypted SNS topic that carries approval requests and callback task tokens."
}

output "execution_table_name" {
  value       = aws_dynamodb_table.orchestration_executions.name
  description = "DynamoDB table used for event-id duplicate suppression and operator-visible execution status."
}

output "approver_policy_arn" {
  value       = aws_iam_policy.step_functions_approver.arn
  description = "Standalone callback policy for an explicitly authorized approver identity. It is not attached automatically."
}
