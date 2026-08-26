# v2.6.0 moves the v2.5.0 root resources under reusable modules.
# Keep these blocks during the upgrade so existing Terraform state can follow the new addresses.

moved {
  from = aws_kms_key.sns
  to   = module.platform.module.notifications.aws_kms_key.sns
}

moved {
  from = aws_kms_alias.sns
  to   = module.platform.module.notifications.aws_kms_alias.sns
}

moved {
  from = aws_sns_topic.incident
  to   = module.platform.module.notifications.aws_sns_topic.incident
}

moved {
  from = aws_sns_topic.approval
  to   = module.platform.module.notifications.aws_sns_topic.approval
}

moved {
  from = aws_sns_topic_subscription.approval_email
  to   = module.platform.module.notifications.aws_sns_topic_subscription.approval_email
}

moved {
  from = aws_cloudwatch_log_group.lambda
  to   = module.platform.module.logging.aws_cloudwatch_log_group.lambda
}

moved {
  from = aws_cloudwatch_log_group.step_functions
  to   = module.platform.module.logging.aws_cloudwatch_log_group.step_functions
}

moved {
  from = aws_cloudwatch_log_group.detection_normalizer
  to   = module.platform.module.logging.aws_cloudwatch_log_group.detection_normalizer
}

moved {
  from = aws_iam_role.lambda
  to   = module.platform.module.iam.aws_iam_role.lambda
}

moved {
  from = aws_iam_role_policy.lambda
  to   = module.platform.module.iam.aws_iam_role_policy.lambda
}

moved {
  from = aws_iam_role.step_functions
  to   = module.platform.module.iam.aws_iam_role.step_functions
}

moved {
  from = aws_iam_role_policy.step_functions
  to   = module.platform.module.iam.aws_iam_role_policy.step_functions
}

moved {
  from = aws_iam_policy.step_functions_approver
  to   = module.platform.module.iam.aws_iam_policy.step_functions_approver
}

moved {
  from = aws_iam_role.detection_normalizer
  to   = module.platform.module.iam.aws_iam_role.detection_normalizer
}

moved {
  from = aws_iam_role_policy.detection_normalizer
  to   = module.platform.module.iam.aws_iam_role_policy.detection_normalizer
}

moved {
  from = aws_lambda_function.action
  to   = module.platform.module.response_actions.aws_lambda_function.action
}

moved {
  from = aws_dynamodb_table.orchestration_executions
  to   = module.platform.module.orchestration.aws_dynamodb_table.executions
}

moved {
  from = aws_sfn_state_machine.ec2_incident_response
  to   = module.platform.module.orchestration.aws_sfn_state_machine.ec2_incident_response
}

moved {
  from = aws_kms_key.ssm_evidence
  to   = module.platform.module.investigation.aws_kms_key.ssm_evidence
}

moved {
  from = aws_kms_alias.ssm_evidence
  to   = module.platform.module.investigation.aws_kms_alias.ssm_evidence
}

moved {
  from = aws_s3_bucket.ssm_evidence
  to   = module.platform.module.investigation.aws_s3_bucket.ssm_evidence
}

moved {
  from = aws_s3_bucket_public_access_block.ssm_evidence
  to   = module.platform.module.investigation.aws_s3_bucket_public_access_block.ssm_evidence
}

moved {
  from = aws_s3_bucket_ownership_controls.ssm_evidence
  to   = module.platform.module.investigation.aws_s3_bucket_ownership_controls.ssm_evidence
}

moved {
  from = aws_s3_bucket_versioning.ssm_evidence
  to   = module.platform.module.investigation.aws_s3_bucket_versioning.ssm_evidence
}

moved {
  from = aws_s3_bucket_server_side_encryption_configuration.ssm_evidence
  to   = module.platform.module.investigation.aws_s3_bucket_server_side_encryption_configuration.ssm_evidence
}

moved {
  from = aws_s3_bucket_lifecycle_configuration.ssm_evidence
  to   = module.platform.module.investigation.aws_s3_bucket_lifecycle_configuration.ssm_evidence
}

moved {
  from = aws_s3_bucket_policy.ssm_evidence
  to   = module.platform.module.investigation.aws_s3_bucket_policy.ssm_evidence
}

moved {
  from = aws_iam_role.ssm_automation
  to   = module.platform.module.investigation.aws_iam_role.ssm_automation
}

moved {
  from = aws_iam_role_policy.ssm_automation
  to   = module.platform.module.investigation.aws_iam_role_policy.ssm_automation
}

moved {
  from = aws_iam_policy.ssm_evidence_node
  to   = module.platform.module.investigation.aws_iam_policy.ssm_evidence_node
}

moved {
  from = aws_ssm_document.collect_linux_evidence
  to   = module.platform.module.investigation.aws_ssm_document.collect_linux_evidence
}

moved {
  from = aws_ssm_document.collect_windows_evidence
  to   = module.platform.module.investigation.aws_ssm_document.collect_windows_evidence
}

moved {
  from = aws_iam_policy.ssm_investigation_operator
  to   = module.platform.module.investigation.aws_iam_policy.ssm_investigation_operator
}

moved {
  from = aws_sqs_queue.detection_dlq
  to   = module.platform.module.event_routing.aws_sqs_queue.detection_dlq
}

moved {
  from = aws_dynamodb_table.detection_dedup
  to   = module.platform.module.event_routing.aws_dynamodb_table.detection_dedup
}

moved {
  from = aws_lambda_function.detection_normalizer
  to   = module.platform.module.event_routing.aws_lambda_function.detection_normalizer
}

moved {
  from = aws_cloudwatch_event_rule.detection
  to   = module.platform.module.event_routing.aws_cloudwatch_event_rule.detection
}

moved {
  from = aws_lambda_permission.eventbridge_detection
  to   = module.platform.module.event_routing.aws_lambda_permission.eventbridge_detection
}

moved {
  from = aws_cloudwatch_event_target.detection
  to   = module.platform.module.event_routing.aws_cloudwatch_event_target.detection
}

moved {
  from = aws_sqs_queue_policy.detection_dlq
  to   = module.platform.module.event_routing.aws_sqs_queue_policy.detection_dlq
}

moved {
  from = aws_cloudwatch_event_archive.detection
  to   = module.platform.module.event_routing.aws_cloudwatch_event_archive.detection
}

moved {
  from = aws_cloudwatch_log_metric_filter.security_signal
  to   = module.platform.module.event_routing.aws_cloudwatch_log_metric_filter.security_signal
}

moved {
  from = aws_cloudwatch_metric_alarm.security_signal
  to   = module.platform.module.event_routing.aws_cloudwatch_metric_alarm.security_signal
}
