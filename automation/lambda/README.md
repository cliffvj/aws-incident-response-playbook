# Lambda Response Action Catalog

Every subdirectory is independently packageable as a Lambda ZIP with handler `app.handler`. Shared helpers are copied into the archive under `aws_ir/` by [`package_lambdas.py`](../scripts/package_lambdas.py).

## Action groups

### Read-only collection

- [`collect_ec2_metadata`](collect_ec2_metadata/README.md)
- [`inspect_s3_public_access`](inspect_s3_public_access/README.md)

### Evidence and notification

- [`snapshot_ebs_volumes`](snapshot_ebs_volumes/README.md)
- [`notify_incident`](notify_incident/README.md)

### EC2 containment and recovery

- [`ensure_quarantine_security_group`](ensure_quarantine_security_group/README.md)
- [`isolate_ec2_instance`](isolate_ec2_instance/README.md)
- [`restore_ec2_security_groups`](restore_ec2_security_groups/README.md)

### IAM containment and recovery

- [`disable_iam_access_key`](disable_iam_access_key/README.md)
- [`restore_iam_access_key`](restore_iam_access_key/README.md)

### S3 containment and recovery

- [`contain_s3_public_access`](contain_s3_public_access/README.md)
- [`restore_s3_public_access`](restore_s3_public_access/README.md)

## Common behavior

- Mutating actions default to dry-run when the field is omitted.
- `expected_account_id` may pin the request to one AWS account.
- Regional targets require an explicit or environment-derived Region.
- `status: no_change` means the requested target state already exists.
- Rollback actions require a manifest and `confirm_restore: true` even for dry-run review.
- Lambda exceptions are deliberate hard failures for invalid identifiers, account or Region mismatches, unsafe quarantine groups, missing resources, and invalid manifests.

See [event contract](../docs/event-contract.md), [idempotency](../docs/idempotency.md), and [rollback manifests](../docs/rollback-manifests.md).
