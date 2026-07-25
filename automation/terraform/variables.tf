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
