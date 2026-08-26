variable "source_root" {
  type = string
}
variable "aws_region" {
  type = string
}
variable "project_name" {
  type = string
}
variable "environment" {
  type = string
}
variable "tags" {
  type = map(string)
}
variable "log_retention_days" {
  type = number
}
variable "lambda_timeout_seconds" {
  type = number
}
variable "lambda_memory_mb" {
  type = number
}
variable "s3_bucket_arns" {
  type = list(string)
}
variable "iam_user_arns" {
  type = list(string)
}
variable "approval_timeout_seconds" {
  type = number
}
variable "approval_email_endpoint" {
  type     = string
  default  = null
  nullable = true
}
variable "step_functions_include_execution_data" {
  type = bool
}
variable "ssm_evidence_bucket_name" {
  type     = string
  default  = null
  nullable = true
}
variable "ssm_evidence_retention_days" {
  type = number
}
variable "ssm_evidence_noncurrent_retention_days" {
  type = number
}
variable "detection_default_route" {
  type = string
}
variable "detection_allowed_account_ids" {
  type = list(string)
}
variable "detection_ignore_principal_arn_prefixes" {
  type = list(string)
}
variable "detection_dedup_ttl_seconds" {
  type = number
}
variable "detection_dlq_retention_seconds" {
  type = number
}
variable "detection_max_event_age_seconds" {
  type = number
}
variable "detection_max_retry_attempts" {
  type = number
}
variable "enable_detection_event_archive" {
  type = bool
}
variable "detection_archive_retention_days" {
  type = number
}
variable "enable_cloudwatch_alarm_routing" {
  type = bool
}
variable "cloudwatch_security_log_group_name" {
  type     = string
  default  = null
  nullable = true
}
variable "permissions_boundary_arn" {
  type     = string
  default  = null
  nullable = true
}
variable "kms_deletion_window_days" {
  type = number
}
