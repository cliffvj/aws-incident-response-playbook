output "function_names" {
  value       = module.platform.function_names
  description = "Deployed Lambda response-action names."
}

output "function_arns" {
  value       = module.platform.function_arns
  description = "Deployed Lambda response-action ARNs."
}

output "incident_topic_arn" {
  value       = module.platform.incident_topic_arn
  description = "KMS-encrypted incident notification topic ARN."
}

output "kms_key_arn" {
  value       = module.platform.notification_kms_key_arn
  description = "KMS key protecting incident and approval notification topics."
}

output "configured_s3_bucket_arns" {
  value       = module.platform.configured_s3_bucket_arns
  description = "S3 bucket ARNs embedded in response-action execution policies."
}

output "configured_iam_user_arns" {
  value       = module.platform.configured_iam_user_arns
  description = "IAM user ARNs embedded in access-key response-action policies."
}

output "state_machine_arn" {
  value       = module.platform.state_machine_arn
  description = "Reference EC2 incident-response state machine ARN."
}

output "state_machine_name" {
  value       = module.platform.state_machine_name
  description = "Reference EC2 incident-response state machine name."
}

output "approval_topic_arn" {
  value       = module.platform.approval_topic_arn
  description = "KMS-encrypted approval topic ARN."
}

output "execution_table_name" {
  value       = module.platform.execution_table_name
  description = "DynamoDB orchestration execution-correlation table name."
}

output "approver_policy_arn" {
  value       = module.platform.approver_policy_arn
  description = "Standalone Step Functions callback approver policy ARN."
}

output "ssm_linux_document_name" {
  value       = module.platform.ssm_linux_document_name
  description = "Linux SSM evidence Automation document name."
}

output "ssm_windows_document_name" {
  value       = module.platform.ssm_windows_document_name
  description = "Windows SSM evidence Automation document name."
}

output "ssm_automation_role_arn" {
  value       = module.platform.ssm_automation_role_arn
  description = "SSM evidence Automation service role ARN."
}

output "ssm_evidence_bucket_name" {
  value       = module.platform.ssm_evidence_bucket_name
  description = "Versioned SSM evidence bucket name."
}

output "ssm_evidence_kms_key_arn" {
  value       = module.platform.ssm_evidence_kms_key_arn
  description = "KMS key protecting SSM evidence."
}

output "ssm_evidence_node_policy_arn" {
  value       = module.platform.ssm_evidence_node_policy_arn
  description = "Reference managed-node evidence-write policy ARN."
}

output "ssm_investigation_operator_policy_arn" {
  value       = module.platform.ssm_investigation_operator_policy_arn
  description = "Reference responder investigation policy ARN."
}

output "detection_normalizer_function_name" {
  value       = module.platform.detection_normalizer_function_name
  description = "Detection normalizer Lambda function name."
}

output "detection_dlq_url" {
  value       = module.platform.detection_dlq_url
  description = "EventBridge target DLQ URL."
}

output "detection_dedup_table_name" {
  value       = module.platform.detection_dedup_table_name
  description = "Detection duplicate-suppression table name."
}
