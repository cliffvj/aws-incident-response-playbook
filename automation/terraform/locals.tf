locals {
  functions = {
    collect_ec2_metadata = ["ec2:DescribeInstances"]
    isolate_ec2_instance = ["ec2:DescribeInstances", "ec2:DescribeSecurityGroups", "ec2:ModifyInstanceAttribute"]
    snapshot_ebs_volumes = ["ec2:DescribeInstances", "ec2:CreateSnapshot", "ec2:CreateTags"]
    disable_iam_access_key = ["iam:GetAccessKeyLastUsed", "iam:UpdateAccessKey"]
    notify_incident = [
      "sns:Publish",
      "kms:Decrypt",
      "kms:GenerateDataKey",
    ]
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
