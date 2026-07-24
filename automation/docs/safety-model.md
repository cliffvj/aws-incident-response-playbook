# Safety Model

## Required controls

- Dedicated lab account before production consideration.
- Explicit resource identifiers; no wildcard discovery followed by mutation.
- `dry_run` defaults to `true` when omitted.
- CloudTrail enabled and CloudWatch log retention configured.
- Change approval for non-dry-run invocation.
- Incident ID attached to logs and created snapshots.
- Rollback plan documented before EC2 isolation or IAM key disablement.

## Important limitations

- Security-group replacement can interrupt all connectivity, including Systems Manager paths that depend on VPC endpoints or internet egress.
- EBS snapshots preserve block-storage state, not memory or every volatile artifact.
- Deactivating an IAM user access key does not revoke already-issued role sessions or credentials belonging to other principals.
- SNS publishing is notification, not durable case management.
