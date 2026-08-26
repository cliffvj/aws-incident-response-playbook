data "aws_partition" "current" {}
data "aws_caller_identity" "current" {}

locals {
  action_names = toset([
    "collect_ec2_metadata",
    "ensure_quarantine_security_group",
    "isolate_ec2_instance",
    "restore_ec2_security_groups",
    "snapshot_ebs_volumes",
    "disable_iam_access_key",
    "restore_iam_access_key",
    "inspect_s3_public_access",
    "contain_s3_public_access",
    "restore_s3_public_access",
    "notify_incident",
  ])

  effective_s3_bucket_arns = length(var.s3_bucket_arns) > 0 ? var.s3_bucket_arns : [
    "arn:${data.aws_partition.current.partition}:s3:::example-incident-bucket-123",
  ]

  effective_iam_user_arns = length(var.iam_user_arns) > 0 ? var.iam_user_arns : [
    "arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:user/incident-lab/*",
  ]

  tags = merge(var.tags, { Environment = var.environment })
}

module "notifications" {
  source = "../notifications"

  project_name             = var.project_name
  tags                     = local.tags
  approval_email_endpoint  = var.approval_email_endpoint
  kms_deletion_window_days = var.kms_deletion_window_days
}

module "logging" {
  source = "../logging"

  project_name      = var.project_name
  action_names      = local.action_names
  retention_in_days = var.log_retention_days
  tags              = local.tags
}

module "iam" {
  source = "../iam"

  project_name             = var.project_name
  aws_region               = var.aws_region
  account_id               = data.aws_caller_identity.current.account_id
  partition                = data.aws_partition.current.partition
  s3_bucket_arns           = local.effective_s3_bucket_arns
  iam_user_arns            = local.effective_iam_user_arns
  incident_topic_arn       = module.notifications.incident_topic_arn
  notification_kms_key_arn = module.notifications.kms_key_arn
  approval_topic_arn       = module.notifications.approval_topic_arn
  permissions_boundary_arn = var.permissions_boundary_arn
  tags                     = local.tags
}

module "response_actions" {
  source = "../response-actions"

  source_root        = var.source_root
  project_name       = var.project_name
  role_arns          = module.iam.lambda_role_arns
  incident_topic_arn = module.notifications.incident_topic_arn
  timeout_seconds    = var.lambda_timeout_seconds
  memory_mb          = var.lambda_memory_mb
  tags               = local.tags

  depends_on = [module.logging]
}

module "orchestration" {
  source = "../orchestration"

  source_root              = var.source_root
  project_name             = var.project_name
  partition                = data.aws_partition.current.partition
  role_arn                 = module.iam.step_functions_role_arn
  function_arns            = module.response_actions.function_arns
  approval_topic_arn       = module.notifications.approval_topic_arn
  log_group_arn            = module.logging.step_functions_log_group_arn
  approval_timeout_seconds = var.approval_timeout_seconds
  include_execution_data   = var.step_functions_include_execution_data
  tags                     = local.tags
}

module "investigation" {
  source = "../investigation"

  source_root               = var.source_root
  project_name              = var.project_name
  aws_region                = var.aws_region
  account_id                = data.aws_caller_identity.current.account_id
  partition                 = data.aws_partition.current.partition
  bucket_name               = var.ssm_evidence_bucket_name
  retention_days            = var.ssm_evidence_retention_days
  noncurrent_retention_days = var.ssm_evidence_noncurrent_retention_days
  permissions_boundary_arn  = var.permissions_boundary_arn
  kms_deletion_window_days  = var.kms_deletion_window_days
  tags                      = local.tags
}

module "event_routing" {
  source = "../event-routing"

  source_root                        = var.source_root
  project_name                       = var.project_name
  aws_region                         = var.aws_region
  account_id                         = data.aws_caller_identity.current.account_id
  partition                          = data.aws_partition.current.partition
  role_arn                           = module.iam.detection_normalizer_role_arn
  state_machine_arn                  = module.orchestration.state_machine_arn
  incident_topic_arn                 = module.notifications.incident_topic_arn
  log_group_name                     = module.logging.detection_normalizer_log_group_name
  default_route                      = var.detection_default_route
  allowed_account_ids                = var.detection_allowed_account_ids
  ignore_principal_arn_prefixes      = var.detection_ignore_principal_arn_prefixes
  dedup_ttl_seconds                  = var.detection_dedup_ttl_seconds
  dlq_retention_seconds              = var.detection_dlq_retention_seconds
  max_event_age_seconds              = var.detection_max_event_age_seconds
  max_retry_attempts                 = var.detection_max_retry_attempts
  enable_event_archive               = var.enable_detection_event_archive
  archive_retention_days             = var.detection_archive_retention_days
  enable_cloudwatch_alarm_routing    = var.enable_cloudwatch_alarm_routing
  cloudwatch_security_log_group_name = var.cloudwatch_security_log_group_name
  tags                               = local.tags

  depends_on = [module.logging]
}
