variable "aws_region" {
  type        = string
  description = "AWS Region for regional automation resources and supported targets."
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Name prefix for the lab automation resources."
  default     = "aws-ir-lab"
}

variable "log_retention_days" {
  type        = number
  description = "CloudWatch Logs retention for Lambda log groups."
  default     = 30
}

variable "lambda_timeout_seconds" {
  type        = number
  description = "Timeout applied to each response-action Lambda function."
  default     = 60
}

variable "lambda_memory_mb" {
  type        = number
  description = "Memory applied to each response-action Lambda function."
  default     = 256
}

variable "s3_bucket_arns" {
  type        = list(string)
  description = "General-purpose S3 bucket ARNs that the inspection, containment, and restoration functions may access. Replace the placeholder before live testing."
  default     = []
}

variable "iam_user_arns" {
  type        = list(string)
  description = "IAM user ARNs or constrained ARN patterns whose access keys may be disabled or restored."
  default     = []
}

variable "tags" {
  type        = map(string)
  description = "Additional tags applied to Terraform-managed resources."
  default     = {}
}

variable "approval_timeout_seconds" {
  type        = number
  description = "Maximum time a live containment or rollback execution waits for a human callback decision."
  default     = 3600

  validation {
    condition     = var.approval_timeout_seconds >= 60 && var.approval_timeout_seconds <= 86400
    error_message = "approval_timeout_seconds must be between 60 and 86400 seconds."
  }
}

variable "approval_email_endpoint" {
  type        = string
  description = "Optional lab-only email endpoint for approval SNS messages. The subscription requires confirmation and exposes sensitive task tokens to that mailbox."
  default     = null
  nullable    = true
}

variable "step_functions_include_execution_data" {
  type        = bool
  description = "Whether Step Functions CloudWatch Logs include execution input/output. Keep false by default because approval task tokens and incident context are sensitive."
  default     = false
}

variable "ssm_evidence_bucket_name" {
  type        = string
  description = "Optional globally unique S3 bucket name for SSM investigation evidence. When null, a name is derived from project, account, and Region."
  default     = null
  nullable    = true
}

variable "ssm_evidence_retention_days" {
  type        = number
  description = "Days before current SSM investigation evidence objects expire. Adjust to the authorized lab retention policy."
  default     = 90

  validation {
    condition     = var.ssm_evidence_retention_days >= 1
    error_message = "ssm_evidence_retention_days must be at least 1 day."
  }
}

variable "ssm_evidence_noncurrent_retention_days" {
  type        = number
  description = "Days before noncurrent versions of SSM investigation evidence expire."
  default     = 30

  validation {
    condition     = var.ssm_evidence_noncurrent_retention_days >= 1
    error_message = "ssm_evidence_noncurrent_retention_days must be at least 1 day."
  }
}

variable "detection_default_route" {
  type        = string
  description = "Default response route for normalized detections: notify_only or read-only triage."
  default     = "notify_only"
  validation {
    condition     = contains(["notify_only", "triage"], var.detection_default_route)
    error_message = "detection_default_route must be notify_only or triage."
  }
}

variable "detection_allowed_account_ids" {
  type        = list(string)
  description = "Optional source-account allowlist for detection events. Empty permits the local account and any intentionally forwarded account."
  default     = []
}

variable "detection_ignore_principal_arn_prefixes" {
  type        = list(string)
  description = "Narrow principal ARN prefixes suppressed by the CloudTrail normalizer to reduce automation loops."
  default     = []
}

variable "detection_dedup_ttl_seconds" {
  type        = number
  description = "Duplicate-suppression TTL for normalized findings."
  default     = 86400
}

variable "detection_dlq_retention_seconds" {
  type        = number
  description = "Retention for undelivered EventBridge target events in the SQS DLQ."
  default     = 1209600
}

variable "detection_max_event_age_seconds" {
  type        = number
  description = "Maximum age EventBridge retries a failed target delivery."
  default     = 3600
}

variable "detection_max_retry_attempts" {
  type        = number
  description = "Maximum EventBridge target retry attempts."
  default     = 12
}

variable "enable_detection_event_archive" {
  type        = bool
  description = "Enable an EventBridge archive for selected security-event sources. Disabled by default for cost and retention control."
  default     = false
}

variable "detection_archive_retention_days" {
  type        = number
  description = "Retention days for the optional EventBridge archive."
  default     = 7
}

variable "enable_cloudwatch_alarm_routing" {
  type        = bool
  description = "Enable routing of generic CloudWatch ALARM state changes. Disabled by default because account-wide alarm routing can be noisy."
  default     = false
}

variable "cloudwatch_security_log_group_name" {
  type        = string
  description = "Optional existing CloudWatch Logs log group on which to create a simple AccessDenied metric filter and alarm."
  default     = null
  nullable    = true
}
