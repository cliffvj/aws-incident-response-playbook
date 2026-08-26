locals {
  network_interface_arns = ["arn:${var.partition}:ec2:${var.aws_region}:${var.account_id}:network-interface/*"]
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

  statements = {
    collect_ec2_metadata = [{ Sid = "ReadTargetInstance", Effect = "Allow", Action = ["ec2:DescribeInstances"], Resource = ["*"] }]
    ensure_quarantine_security_group = [
      { Sid = "InspectSecurityGroups", Effect = "Allow", Action = ["ec2:DescribeSecurityGroups"], Resource = ["*"] },
      { Sid = "CreateAndPrepareQuarantineGroup", Effect = "Allow", Action = ["ec2:CreateSecurityGroup", "ec2:CreateTags", "ec2:RevokeSecurityGroupIngress", "ec2:RevokeSecurityGroupEgress"], Resource = ["*"] },
    ]
    isolate_ec2_instance = [
      { Sid = "InspectInstanceAndSecurityGroup", Effect = "Allow", Action = ["ec2:DescribeInstances", "ec2:DescribeSecurityGroups"], Resource = ["*"] },
      { Sid = "IsolateNetworkInterfaces", Effect = "Allow", Action = ["ec2:ModifyNetworkInterfaceAttribute"], Resource = local.network_interface_arns },
    ]
    restore_ec2_security_groups = [
      { Sid = "InspectNetworkInterfaces", Effect = "Allow", Action = ["ec2:DescribeNetworkInterfaces"], Resource = ["*"] },
      { Sid = "RestoreNetworkInterfaceGroups", Effect = "Allow", Action = ["ec2:ModifyNetworkInterfaceAttribute"], Resource = local.network_interface_arns },
    ]
    snapshot_ebs_volumes = [{ Sid = "CreateIncidentSnapshots", Effect = "Allow", Action = ["ec2:DescribeInstances", "ec2:DescribeSnapshots", "ec2:CreateSnapshot", "ec2:CreateTags"], Resource = ["*"] }]
    disable_iam_access_key = [
      { Sid = "ReadAccessKeyLastUsed", Effect = "Allow", Action = ["iam:GetAccessKeyLastUsed"], Resource = ["*"] },
      { Sid = "InspectAndDisableApprovedUserKeys", Effect = "Allow", Action = ["iam:ListAccessKeys", "iam:UpdateAccessKey"], Resource = var.iam_user_arns },
    ]
    restore_iam_access_key   = [{ Sid = "InspectAndRestoreApprovedUserKeys", Effect = "Allow", Action = ["iam:ListAccessKeys", "iam:UpdateAccessKey"], Resource = var.iam_user_arns }]
    inspect_s3_public_access = [{ Sid = "InspectApprovedBucketPublicAccess", Effect = "Allow", Action = ["s3:GetBucketLocation", "s3:GetBucketPublicAccessBlock", "s3:GetBucketPolicyStatus", "s3:GetBucketPolicy", "s3:GetBucketAcl", "s3:GetBucketOwnershipControls"], Resource = var.s3_bucket_arns }]
    contain_s3_public_access = [{ Sid = "InspectAndContainApprovedBucketPublicAccess", Effect = "Allow", Action = ["s3:GetBucketLocation", "s3:GetBucketPublicAccessBlock", "s3:GetBucketPolicyStatus", "s3:GetBucketPolicy", "s3:GetBucketAcl", "s3:GetBucketOwnershipControls", "s3:PutBucketPublicAccessBlock"], Resource = var.s3_bucket_arns }]
    restore_s3_public_access = [{ Sid = "InspectAndRestoreApprovedBucketPublicAccess", Effect = "Allow", Action = ["s3:GetBucketLocation", "s3:GetBucketPublicAccessBlock", "s3:GetBucketPolicyStatus", "s3:GetBucketPolicy", "s3:GetBucketAcl", "s3:GetBucketOwnershipControls", "s3:PutBucketPublicAccessBlock"], Resource = var.s3_bucket_arns }]
    notify_incident = [
      { Sid = "PublishIncidentNotification", Effect = "Allow", Action = ["sns:Publish"], Resource = [var.incident_topic_arn] },
      { Sid = "UseIncidentTopicKey", Effect = "Allow", Action = ["kms:Decrypt", "kms:GenerateDataKey"], Resource = [var.notification_kms_key_arn] },
    ]
  }
}

resource "aws_iam_role" "lambda" {
  for_each             = local.action_names
  name                 = "${var.project_name}-${replace(each.key, "_", "-")}-role"
  permissions_boundary = var.permissions_boundary_arn
  assume_role_policy   = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" }, Action = "sts:AssumeRole" }] })
  tags                 = var.tags
}

resource "aws_iam_role_policy" "lambda" {
  for_each = local.action_names
  name     = "${var.project_name}-${replace(each.key, "_", "-")}-policy"
  role     = aws_iam_role.lambda[each.key].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = concat([
      { Sid = "Logs", Effect = "Allow", Action = ["logs:CreateLogStream", "logs:PutLogEvents"], Resource = "arn:${var.partition}:logs:${var.aws_region}:${var.account_id}:log-group:/aws/lambda/${var.project_name}-*:*" }
    ], local.statements[each.key])
  })
}

resource "aws_iam_role" "step_functions" {
  name                 = "${var.project_name}-step-functions-role"
  permissions_boundary = var.permissions_boundary_arn
  assume_role_policy   = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "states.amazonaws.com" }, Action = "sts:AssumeRole" }] })
  tags                 = var.tags
}

resource "aws_iam_role_policy" "step_functions" {
  name = "${var.project_name}-step-functions-policy"
  role = aws_iam_role.step_functions.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Sid = "InvokeResponseActions", Effect = "Allow", Action = ["lambda:InvokeFunction"], Resource = [for name in local.action_names : "arn:${var.partition}:lambda:${var.aws_region}:${var.account_id}:function:${var.project_name}-${replace(name, "_", "-")}"] },
      { Sid = "PublishApprovalRequests", Effect = "Allow", Action = ["sns:Publish"], Resource = [var.approval_topic_arn] },
      { Sid = "UseApprovalTopicKey", Effect = "Allow", Action = ["kms:Decrypt", "kms:GenerateDataKey*"], Resource = [var.notification_kms_key_arn] },
      { Sid = "MaintainExecutionCorrelation", Effect = "Allow", Action = ["dynamodb:PutItem", "dynamodb:UpdateItem"], Resource = ["arn:${var.partition}:dynamodb:${var.aws_region}:${var.account_id}:table/${var.project_name}-orchestration-executions"] },
      { Sid = "StepFunctionsLogDelivery", Effect = "Allow", Action = ["logs:CreateLogDelivery", "logs:GetLogDelivery", "logs:UpdateLogDelivery", "logs:DeleteLogDelivery", "logs:ListLogDeliveries", "logs:PutResourcePolicy", "logs:DescribeResourcePolicies", "logs:DescribeLogGroups"], Resource = ["*"] },
    ]
  })
}

resource "aws_iam_policy" "step_functions_approver" {
  name        = "${var.project_name}-step-functions-approver"
  description = "Allows an explicitly authorized responder to resolve Step Functions callback task tokens. Not attached automatically."
  policy      = jsonencode({ Version = "2012-10-17", Statement = [{ Sid = "ResolveApprovalTaskTokens", Effect = "Allow", Action = ["states:SendTaskSuccess", "states:SendTaskFailure"], Resource = "*" }] })
  tags        = var.tags
}

resource "aws_iam_role" "detection_normalizer" {
  name                 = "${var.project_name}-detection-normalizer-role"
  permissions_boundary = var.permissions_boundary_arn
  assume_role_policy   = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Service = "lambda.amazonaws.com" }, Action = "sts:AssumeRole" }] })
  tags                 = var.tags
}

resource "aws_iam_role_policy" "detection_normalizer" {
  name = "${var.project_name}-detection-normalizer-policy"
  role = aws_iam_role.detection_normalizer.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Sid = "Logs", Effect = "Allow", Action = ["logs:CreateLogStream", "logs:PutLogEvents"], Resource = "arn:${var.partition}:logs:${var.aws_region}:${var.account_id}:log-group:/aws/lambda/${var.project_name}-normalize-security-event:*" },
      { Sid = "AcquireDeduplicationKey", Effect = "Allow", Action = ["dynamodb:PutItem"], Resource = "arn:${var.partition}:dynamodb:${var.aws_region}:${var.account_id}:table/${var.project_name}-detection-dedup" },
      { Sid = "StartReadOnlyTriage", Effect = "Allow", Action = ["states:StartExecution"], Resource = "arn:${var.partition}:states:${var.aws_region}:${var.account_id}:stateMachine:${var.project_name}-ec2-incident-response" },
      { Sid = "PublishNotifyOnly", Effect = "Allow", Action = ["sns:Publish"], Resource = var.incident_topic_arn },
      { Sid = "UseIncidentTopicKey", Effect = "Allow", Action = ["kms:Decrypt", "kms:GenerateDataKey"], Resource = var.notification_kms_key_arn },
    ]
  })
}
