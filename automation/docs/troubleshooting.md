# Troubleshooting

| Symptom | Likely cause | Check |
|---|---|---|
| `expected_account_id ... does not match` | Wrong credentials, assumed role, or event account | `aws sts get-caller-identity`, profile, role session |
| Region validation failure | Event Region does not match target or environment | Lambda Region, event `region`, S3 bucket Region |
| `AccessDenied` | Execution role lacks an action, resource ARN, tag condition, KMS permission, or organization policy permits a deny | CloudTrail error, generated IAM policy, permissions boundary, SCP, key policy |
| Isolation rejects quarantine group | Group is in another VPC or still has ingress/egress rules | `describe-security-groups`, VPC ID, default egress removal |
| EC2 restore rejects manifest | Checksum, account, Region, incident, instance, or interface state differs | Preserve exact JSON; do not edit the manifest |
| EC2 restore cannot find a group | Original group was deleted after isolation | Recreate and review manually; automated restore does not guess |
| Snapshot returns `no_change` | Matching incident/source-volume snapshot already exists | Snapshot tags and state |
| Snapshot remains pending | EBS operation is asynchronous | `describe-snapshots`, volume size, service events |
| IAM key action says key does not belong to user | Wrong user/key pair or unsupported root access key | `list-access-keys --user-name ...`, CloudTrail |
| IAM restore is unsafe | Key may still be compromised | Prefer new key, rotate dependencies, delete old key |
| S3 inspection fails on policy or ACL | Missing read permission, wrong owner, unsupported bucket type, or explicit deny | Bucket ARN, expected owner, bucket type, policy/SCP |
| S3 containment returns `no_change` | All four bucket-level controls are already enabled | Current Block Public Access response |
| S3 restore deletes Block Public Access | Original manifest recorded that no bucket-level configuration existed | Review manifest before approval; account-level controls may remain |
| SNS publish fails | Topic policy, KMS permission, ARN account/Region mismatch | Topic ARN, key policy, CloudTrail |
| Local tests work but Lambda fails | Packaging path, handler, runtime, or role policy mismatch | ZIP contents, `app.handler`, Python runtime, CloudWatch Logs |

## Diagnostic commands

```bash
python3 automation/scripts/validate_json.py
python3 automation/scripts/check_action_contracts.py
python3 automation/scripts/package_lambdas.py
python3 -m unittest discover -s automation/tests -p 'test_*.py'
```

For an AWS failure, record the exception code, Lambda request ID, CloudTrail event ID, target resource, account, Region, and whether a write may have been accepted before retrying.
