locals {
  evidence_bucket_name = var.bucket_name != null ? var.bucket_name : lower("${substr(replace(var.project_name, "_", "-"), 0, 20)}-${var.account_id}-${var.aws_region}-ssm-evidence")
}

resource "aws_kms_key" "ssm_evidence" {
  description             = "KMS key for ${var.project_name} Systems Manager investigation evidence"
  deletion_window_in_days = var.kms_deletion_window_days
  enable_key_rotation     = true
  tags                    = var.tags
}

resource "aws_kms_alias" "ssm_evidence" {
  name          = "alias/${var.project_name}-ssm-evidence"
  target_key_id = aws_kms_key.ssm_evidence.key_id
}

resource "aws_s3_bucket" "ssm_evidence" {
  bucket = local.evidence_bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_public_access_block" "ssm_evidence" {
  bucket                  = aws_s3_bucket.ssm_evidence.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_ownership_controls" "ssm_evidence" {
  bucket = aws_s3_bucket.ssm_evidence.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_versioning" "ssm_evidence" {
  bucket = aws_s3_bucket.ssm_evidence.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "ssm_evidence" {
  bucket = aws_s3_bucket.ssm_evidence.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.ssm_evidence.arn
      sse_algorithm     = "aws:kms"
    }

    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "ssm_evidence" {
  bucket = aws_s3_bucket.ssm_evidence.id

  rule {
    id     = "incident-evidence-retention"
    status = "Enabled"

    filter {}

    expiration {
      days = var.retention_days
    }

    noncurrent_version_expiration {
      noncurrent_days = var.noncurrent_retention_days
    }
  }
}

data "aws_iam_policy_document" "ssm_evidence_bucket" {
  statement {
    sid    = "DenyInsecureTransport"
    effect = "Deny"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.ssm_evidence.arn,
      "${aws_s3_bucket.ssm_evidence.arn}/*",
    ]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "ssm_evidence" {
  bucket = aws_s3_bucket.ssm_evidence.id
  policy = data.aws_iam_policy_document.ssm_evidence_bucket.json
}

resource "aws_iam_role" "ssm_automation" {
  name                 = "${var.project_name}-ssm-automation-role"
  permissions_boundary = var.permissions_boundary_arn

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ssm.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "ssm_automation" {
  name = "${var.project_name}-ssm-automation-policy"
  role = aws_iam_role.ssm_automation.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "InspectManagedNode"
        Effect   = "Allow"
        Action   = ["ssm:DescribeInstanceInformation"]
        Resource = "*"
      },
      {
        Sid    = "RunApprovedCollectionDocuments"
        Effect = "Allow"
        Action = ["ssm:SendCommand"]
        Resource = [
          "arn:${var.partition}:ssm:${var.aws_region}::document/AWS-RunShellScript",
          "arn:${var.partition}:ssm:${var.aws_region}::document/AWS-RunPowerShellScript",
          "arn:${var.partition}:ec2:${var.aws_region}:${var.account_id}:instance/*",
        ]
      },
      {
        Sid      = "ReadRunCommandStatus"
        Effect   = "Allow"
        Action   = ["ssm:GetCommandInvocation", "ssm:ListCommandInvocations"]
        Resource = "*"
      },
      {
        Sid      = "ListEvidencePrefix"
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = aws_s3_bucket.ssm_evidence.arn
        Condition = {
          StringLike = {
            "s3:prefix" = ["incidents/*"]
          }
        }
      },
      {
        Sid      = "ReadAndFinalizeEvidence"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:GetObjectVersion", "s3:PutObject"]
        Resource = ["${aws_s3_bucket.ssm_evidence.arn}/incidents/*"]
      },
      {
        Sid      = "UseEvidenceKey"
        Effect   = "Allow"
        Action   = ["kms:Decrypt", "kms:Encrypt", "kms:GenerateDataKey"]
        Resource = [aws_kms_key.ssm_evidence.arn]
      },
    ]
  })
}

resource "aws_iam_policy" "ssm_evidence_node" {
  name        = "${var.project_name}-ssm-evidence-node"
  description = "Allows authorized SSM managed EC2 nodes to write investigation output. Not attached automatically."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ReadEvidenceBucketConfiguration"
        Effect   = "Allow"
        Action   = ["s3:GetBucketLocation", "s3:GetEncryptionConfiguration"]
        Resource = aws_s3_bucket.ssm_evidence.arn
      },
      {
        Sid      = "WriteRunCommandEvidence"
        Effect   = "Allow"
        Action   = ["s3:PutObject", "s3:AbortMultipartUpload"]
        Resource = "${aws_s3_bucket.ssm_evidence.arn}/incidents/*"
      },
      {
        Sid      = "UseEvidenceKeyForWrites"
        Effect   = "Allow"
        Action   = ["kms:Encrypt", "kms:GenerateDataKey"]
        Resource = aws_kms_key.ssm_evidence.arn
      },
    ]
  })

  tags = var.tags
}

resource "aws_ssm_document" "collect_linux_evidence" {
  name            = "${var.project_name}-collect-linux-evidence"
  document_type   = "Automation"
  document_format = "JSON"
  content         = file("${var.source_root}/ssm/collect-linux-evidence.json")
  tags            = var.tags
}

resource "aws_ssm_document" "collect_windows_evidence" {
  name            = "${var.project_name}-collect-windows-evidence"
  document_type   = "Automation"
  document_format = "JSON"
  content         = file("${var.source_root}/ssm/collect-windows-evidence.json")
  tags            = var.tags
}

resource "aws_iam_policy" "ssm_investigation_operator" {
  name        = "${var.project_name}-ssm-investigation-operator"
  description = "Reference responder policy for starting investigation Automation and reading evidence. Not attached automatically."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "StartApprovedInvestigationRunbooks"
        Effect   = "Allow"
        Action   = ["ssm:StartAutomationExecution"]
        Resource = [aws_ssm_document.collect_linux_evidence.arn, aws_ssm_document.collect_windows_evidence.arn]
      },
      {
        Sid      = "InspectAutomationExecutions"
        Effect   = "Allow"
        Action   = ["ssm:GetAutomationExecution", "ssm:DescribeAutomationExecutions", "ssm:DescribeAutomationStepExecutions"]
        Resource = "*"
      },
      {
        Sid      = "PassOnlyInvestigationAutomationRole"
        Effect   = "Allow"
        Action   = ["iam:PassRole"]
        Resource = aws_iam_role.ssm_automation.arn
        Condition = {
          StringEquals = {
            "iam:PassedToService" = "ssm.amazonaws.com"
          }
        }
      },
      {
        Sid      = "ListEvidence"
        Effect   = "Allow"
        Action   = ["s3:ListBucket"]
        Resource = aws_s3_bucket.ssm_evidence.arn
      },
      {
        Sid      = "ReadEvidence"
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:GetObjectVersion"]
        Resource = "${aws_s3_bucket.ssm_evidence.arn}/incidents/*"
      },
      {
        Sid      = "DecryptEvidence"
        Effect   = "Allow"
        Action   = ["kms:Decrypt"]
        Resource = aws_kms_key.ssm_evidence.arn
      },
    ]
  })

  tags = var.tags
}
