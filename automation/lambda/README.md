# Lambda Action Catalog

| Function | Required action-specific fields | Write API |
|---|---|---|
| `collect_ec2_metadata` | `instance_id` | None |
| `isolate_ec2_instance` | `instance_id`, `quarantine_security_group_id` | `ModifyInstanceAttribute` |
| `snapshot_ebs_volumes` | `instance_id` | `CreateSnapshot` |
| `disable_iam_access_key` | `user_name`, `access_key_id` | `UpdateAccessKey` |
| `notify_incident` | `severity`, `message`; topic via event or environment | `Publish` |

Each function imports the local `aws_ir` shared package. Use `automation/scripts/package_lambdas.py` or Terraform to build deployment archives.
