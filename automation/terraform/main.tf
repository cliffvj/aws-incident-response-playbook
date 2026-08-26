module "platform" {
  source = "./modules/platform"

  source_root = abspath("${path.module}/..")

  aws_region         = var.aws_region
  project_name       = var.project_name
  environment        = var.deployment_environment
  tags               = local.common_tags
  log_retention_days = var.log_retention_days

  lambda_timeout_seconds = var.lambda_timeout_seconds
  lambda_memory_mb       = var.lambda_memory_mb
  s3_bucket_arns         = var.s3_bucket_arns
  iam_user_arns          = var.iam_user_arns

  approval_timeout_seconds              = var.approval_timeout_seconds
  approval_email_endpoint               = var.approval_email_endpoint
  step_functions_include_execution_data = var.step_functions_include_execution_data

  ssm_evidence_bucket_name               = var.ssm_evidence_bucket_name
  ssm_evidence_retention_days            = var.ssm_evidence_retention_days
  ssm_evidence_noncurrent_retention_days = var.ssm_evidence_noncurrent_retention_days

  detection_default_route                 = var.detection_default_route
  detection_allowed_account_ids           = var.detection_allowed_account_ids
  detection_ignore_principal_arn_prefixes = var.detection_ignore_principal_arn_prefixes
  detection_dedup_ttl_seconds             = var.detection_dedup_ttl_seconds
  detection_dlq_retention_seconds         = var.detection_dlq_retention_seconds
  detection_max_event_age_seconds         = var.detection_max_event_age_seconds
  detection_max_retry_attempts            = var.detection_max_retry_attempts
  enable_detection_event_archive          = var.enable_detection_event_archive
  detection_archive_retention_days        = var.detection_archive_retention_days
  enable_cloudwatch_alarm_routing         = var.enable_cloudwatch_alarm_routing
  cloudwatch_security_log_group_name      = var.cloudwatch_security_log_group_name

  permissions_boundary_arn = var.permissions_boundary_arn
  kms_deletion_window_days = var.kms_deletion_window_days
}
