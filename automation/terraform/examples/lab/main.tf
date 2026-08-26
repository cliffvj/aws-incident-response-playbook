terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 7.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.4, < 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

module "aws_ir" {
  source = "../../modules/platform"

  source_root  = abspath("${path.module}/../../..")
  aws_region   = var.aws_region
  project_name = "aws-ir-lab"
  environment  = "lab"
  tags = {
    Example = "lab"
  }

  log_retention_days       = 14
  lambda_timeout_seconds   = 60
  lambda_memory_mb         = 256
  s3_bucket_arns           = []
  iam_user_arns            = []
  approval_timeout_seconds = 3600
  approval_email_endpoint  = null

  step_functions_include_execution_data = false

  ssm_evidence_bucket_name               = null
  ssm_evidence_retention_days            = 14
  ssm_evidence_noncurrent_retention_days = 30

  detection_default_route                 = "notify_only"
  detection_allowed_account_ids           = []
  detection_ignore_principal_arn_prefixes = []
  detection_dedup_ttl_seconds             = 86400
  detection_dlq_retention_seconds         = 1209600
  detection_max_event_age_seconds         = 3600
  detection_max_retry_attempts            = 12
  enable_detection_event_archive          = false
  detection_archive_retention_days        = 7
  enable_cloudwatch_alarm_routing         = false
  cloudwatch_security_log_group_name      = null

  permissions_boundary_arn = null
  kms_deletion_window_days = 7
}
