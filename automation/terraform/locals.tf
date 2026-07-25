locals {
  s3_bucket_arns_effective = length(var.s3_bucket_arns) > 0 ? var.s3_bucket_arns : [
    "arn:${data.aws_partition.current.partition}:s3:::example-incident-bucket-123"
  ]

  iam_user_arns_effective = length(var.iam_user_arns) > 0 ? var.iam_user_arns : [
    "arn:${data.aws_partition.current.partition}:iam::${data.aws_caller_identity.current.account_id}:user/incident-lab/*"
  ]

  network_interface_arns = [
    "arn:${data.aws_partition.current.partition}:ec2:${var.aws_region}:${data.aws_caller_identity.current.account_id}:network-interface/*"
  ]

  functions = {
    collect_ec2_metadata = {
      statements = [{
        Sid      = "ReadTargetInstance"
        Effect   = "Allow"
        Action   = ["ec2:DescribeInstances"]
        Resource = ["*"]
      }]
    }

    ensure_quarantine_security_group = {
      statements = [
        {
          Sid      = "InspectSecurityGroups"
          Effect   = "Allow"
          Action   = ["ec2:DescribeSecurityGroups"]
          Resource = ["*"]
        },
        {
          Sid    = "CreateAndPrepareQuarantineGroup"
          Effect = "Allow"
          Action = [
            "ec2:CreateSecurityGroup",
            "ec2:CreateTags",
            "ec2:RevokeSecurityGroupIngress",
            "ec2:RevokeSecurityGroupEgress",
          ]
          Resource = ["*"]
        }
      ]
    }

    isolate_ec2_instance = {
      statements = [
        {
          Sid      = "InspectInstanceAndSecurityGroup"
          Effect   = "Allow"
          Action   = ["ec2:DescribeInstances", "ec2:DescribeSecurityGroups"]
          Resource = ["*"]
        },
        {
          Sid      = "IsolateNetworkInterfaces"
          Effect   = "Allow"
          Action   = ["ec2:ModifyNetworkInterfaceAttribute"]
          Resource = local.network_interface_arns
        }
      ]
    }

    restore_ec2_security_groups = {
      statements = [
        {
          Sid      = "InspectNetworkInterfaces"
          Effect   = "Allow"
          Action   = ["ec2:DescribeNetworkInterfaces"]
          Resource = ["*"]
        },
        {
          Sid      = "RestoreNetworkInterfaceGroups"
          Effect   = "Allow"
          Action   = ["ec2:ModifyNetworkInterfaceAttribute"]
          Resource = local.network_interface_arns
        }
      ]
    }

    snapshot_ebs_volumes = {
      statements = [{
        Sid    = "CreateIncidentSnapshots"
        Effect = "Allow"
        Action = [
          "ec2:DescribeInstances",
          "ec2:DescribeSnapshots",
          "ec2:CreateSnapshot",
          "ec2:CreateTags",
        ]
        Resource = ["*"]
      }]
    }

    disable_iam_access_key = {
      statements = [
        {
          Sid      = "ReadAccessKeyLastUsed"
          Effect   = "Allow"
          Action   = ["iam:GetAccessKeyLastUsed"]
          Resource = ["*"]
        },
        {
          Sid      = "InspectAndDisableApprovedUserKeys"
          Effect   = "Allow"
          Action   = ["iam:ListAccessKeys", "iam:UpdateAccessKey"]
          Resource = local.iam_user_arns_effective
        }
      ]
    }

    restore_iam_access_key = {
      statements = [{
        Sid      = "InspectAndRestoreApprovedUserKeys"
        Effect   = "Allow"
        Action   = ["iam:ListAccessKeys", "iam:UpdateAccessKey"]
        Resource = local.iam_user_arns_effective
      }]
    }

    inspect_s3_public_access = {
      statements = [{
        Sid    = "InspectApprovedBucketPublicAccess"
        Effect = "Allow"
        Action = [
          "s3:GetBucketLocation",
          "s3:GetBucketPublicAccessBlock",
          "s3:GetBucketPolicyStatus",
          "s3:GetBucketPolicy",
          "s3:GetBucketAcl",
          "s3:GetBucketOwnershipControls",
        ]
        Resource = local.s3_bucket_arns_effective
      }]
    }

    contain_s3_public_access = {
      statements = [{
        Sid    = "InspectAndContainApprovedBucketPublicAccess"
        Effect = "Allow"
        Action = [
          "s3:GetBucketLocation",
          "s3:GetBucketPublicAccessBlock",
          "s3:GetBucketPolicyStatus",
          "s3:GetBucketPolicy",
          "s3:GetBucketAcl",
          "s3:GetBucketOwnershipControls",
          "s3:PutBucketPublicAccessBlock",
        ]
        Resource = local.s3_bucket_arns_effective
      }]
    }

    restore_s3_public_access = {
      statements = [{
        Sid    = "InspectAndRestoreApprovedBucketPublicAccess"
        Effect = "Allow"
        Action = [
          "s3:GetBucketLocation",
          "s3:GetBucketPublicAccessBlock",
          "s3:GetBucketPolicyStatus",
          "s3:GetBucketPolicy",
          "s3:GetBucketAcl",
          "s3:GetBucketOwnershipControls",
          "s3:PutBucketPublicAccessBlock",
        ]
        Resource = local.s3_bucket_arns_effective
      }]
    }

    notify_incident = {
      statements = [
        {
          Sid      = "PublishIncidentNotification"
          Effect   = "Allow"
          Action   = ["sns:Publish"]
          Resource = [aws_sns_topic.incident.arn]
        },
        {
          Sid      = "UseIncidentTopicKey"
          Effect   = "Allow"
          Action   = ["kms:Decrypt", "kms:GenerateDataKey"]
          Resource = [aws_kms_key.sns.arn]
        }
      ]
    }
  }

  common_tags = merge(
    {
      Project   = var.project_name
      ManagedBy = "Terraform"
      Purpose   = "IncidentResponseLab"
    },
    var.tags,
  )
}
