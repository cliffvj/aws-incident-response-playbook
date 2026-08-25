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

## Orchestration permissions

| Principal | Permissions | Scope / reason |
|---|---|---|
| Step Functions execution role | `lambda:InvokeFunction` | Six EC2 orchestration action functions only |
| Step Functions execution role | `sns:Publish` | Dedicated approval SNS topic only |
| Step Functions execution role | `kms:Decrypt`, `kms:GenerateDataKey` | KMS key protecting the approval topic |
| Step Functions execution role | `dynamodb:PutItem`, `dynamodb:UpdateItem` | Execution-correlation table only |
| Step Functions execution role | CloudWatch Logs delivery APIs | `Resource: "*"` where AWS log-delivery APIs do not support useful resource scoping |
| Dedicated human approver role | `states:SendTaskSuccess`, `states:SendTaskFailure` | `Resource: "*"`; callback APIs rely on the task token and do not expose resource-level state-machine scoping |

Do not attach the approver policy to the state-machine role, Lambda roles, or broad responder groups.

## Systems Manager investigation

| Principal / component | AWS actions | Resource scope | Why |
|---|---|---|---|
| SSM Automation execution role | `ssm:DescribeInstanceInformation` | `*` | Verify the node is managed, Online, and on the expected platform |
| SSM Automation execution role | `ssm:SendCommand` | `AWS-RunShellScript`, `AWS-RunPowerShellScript`, and EC2 instances in the deployment account/Region | Run only the read-only host collection commands |
| SSM Automation execution role | `ssm:GetCommandInvocation`, `ssm:ListCommandInvocations` | `*` | Observe command status/results |
| SSM Automation execution role | `s3:ListBucket` | Evidence bucket and `incidents/*` prefix | Discover Run Command output for hashing |
| SSM Automation execution role | `s3:GetObject`, `s3:GetObjectVersion`, `s3:PutObject` | Evidence `incidents/*` objects | Read command output and write integrity manifest |
| SSM Automation execution role | `kms:Decrypt`, `kms:Encrypt`, `kms:GenerateDataKey` | Evidence KMS key | Hash encrypted objects and write the manifest |
| Target EC2 instance role (supplemental policy) | `s3:GetBucketLocation`, `s3:GetEncryptionConfiguration`, `s3:PutObject`, `s3:AbortMultipartUpload` | Evidence bucket / `incidents/*` | Let SSM Agent write Run Command output |
| Target EC2 instance role (supplemental policy) | `kms:Encrypt`, `kms:GenerateDataKey` | Evidence KMS key | Support SSE-KMS output writes |
| Authorized responder | `ssm:StartAutomationExecution` | Only the two deployed investigation documents | Start evidence collection |
| Authorized responder | `iam:PassRole` | Only the SSM Automation execution role, passed to `ssm.amazonaws.com` | Allow Automation to assume its reviewed role |
| Authorized responder | `ssm:GetAutomationExecution`, execution-description APIs | `*` | Track progress and partial failures |
| Authorized responder | `s3:ListBucket`, `s3:GetObject`, `s3:GetObjectVersion`, `kms:Decrypt` | Evidence bucket/key | Retrieve and verify evidence |

> The target node still needs its normal Systems Manager managed-node permissions. The evidence-write policy supplements those permissions; it does not replace them.
