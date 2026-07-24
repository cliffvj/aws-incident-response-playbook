# Troubleshooting

| Symptom | Likely cause | Check |
|---|---|---|
| `AccessDenied` | Execution role lacks an action or condition does not match | CloudTrail error, IAM policy, resource tags |
| Instance isolation fails | Quarantine SG is in another VPC | Compare instance VPC and SG VPC |
| Snapshot function returns no volumes | Instance uses instance store only or metadata is stale | EC2 block-device mappings |
| IAM key disable fails | Wrong user/key pair or root access key | `GetAccessKeyLastUsed`, IAM user inventory |
| SNS publish fails | Topic policy, KMS permission, or wrong Region | Topic ARN, key policy, CloudTrail |
| Test works locally but not in Lambda | Packaging path or handler mismatch | ZIP contents and handler setting |
