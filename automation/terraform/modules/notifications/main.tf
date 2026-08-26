resource "aws_kms_key" "sns" {
  description             = "KMS key for ${var.project_name} incident and approval notifications"
  deletion_window_in_days = var.kms_deletion_window_days
  enable_key_rotation     = true
  tags                    = var.tags
}

resource "aws_kms_alias" "sns" {
  name          = "alias/${var.project_name}-sns"
  target_key_id = aws_kms_key.sns.key_id
}

resource "aws_sns_topic" "incident" {
  name              = "${var.project_name}-notifications"
  kms_master_key_id = aws_kms_key.sns.arn
  tags              = var.tags
}

resource "aws_sns_topic" "approval" {
  name              = "${var.project_name}-approvals"
  kms_master_key_id = aws_kms_key.sns.arn
  tags              = var.tags
}

resource "aws_sns_topic_subscription" "approval_email" {
  count     = var.approval_email_endpoint == null ? 0 : 1
  topic_arn = aws_sns_topic.approval.arn
  protocol  = "email"
  endpoint  = var.approval_email_endpoint
}
