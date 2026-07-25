# Permissions Matrix

| Function | Read permissions | Write permissions | Primary resource scope |
|---|---|---|---|
| `collect_ec2_metadata` | `ec2:DescribeInstances` | None | Selected account and Region |
| `ensure_quarantine_security_group` | `ec2:DescribeSecurityGroups` | `ec2:CreateSecurityGroup`, `ec2:CreateTags`, `ec2:RevokeSecurityGroupIngress`, `ec2:RevokeSecurityGroupEgress` | Approved VPC and managed security groups |
| `isolate_ec2_instance` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups` | `ec2:ModifyNetworkInterfaceAttribute` | Target instance network interfaces |
| `restore_ec2_security_groups` | `ec2:DescribeNetworkInterfaces` | `ec2:ModifyNetworkInterfaceAttribute` | Interfaces in the validated manifest |
| `snapshot_ebs_volumes` | `ec2:DescribeInstances`, `ec2:DescribeSnapshots` | `ec2:CreateSnapshot`, `ec2:CreateTags` | Attached source volumes and created snapshots |
| `disable_iam_access_key` | `iam:ListAccessKeys`, `iam:GetAccessKeyLastUsed` | `iam:UpdateAccessKey` | Approved IAM user ARNs |
| `restore_iam_access_key` | `iam:ListAccessKeys` | `iam:UpdateAccessKey` | Approved IAM user ARNs |
| `inspect_s3_public_access` | S3 bucket location, Block Public Access, policy status, policy, ACL, and ownership controls | None | Approved bucket ARNs |
| `contain_s3_public_access` | Same as inspection | `s3:PutBucketPublicAccessBlock` | Approved bucket ARNs |
| `restore_s3_public_access` | Same as inspection | `s3:PutBucketPublicAccessBlock` | Approved bucket ARNs |
| `notify_incident` | None | `sns:Publish`; KMS permissions when the topic uses a customer-managed key | Configured incident topic and key |
| All Lambda functions | None | CloudWatch Logs stream and event writes | Their own log group |

`sts:GetCallerIdentity` is used to compare the invocation's optional `expected_account_id` with the actual caller account. Review AWS STS and organizational policy behavior in the deployment environment.
