# Permissions Matrix

| Function | Required actions |
|---|---|
| collect metadata | `ec2:DescribeInstances` |
| isolate EC2 | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `ec2:ModifyInstanceAttribute` |
| snapshot EBS | `ec2:DescribeInstances`, `ec2:CreateSnapshot`, `ec2:CreateTags` |
| disable IAM key | `iam:GetAccessKeyLastUsed`, `iam:UpdateAccessKey` |
| notify incident | `sns:Publish` |
| all Lambda functions | CloudWatch Logs permissions through execution role |
