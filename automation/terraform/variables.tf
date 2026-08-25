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
