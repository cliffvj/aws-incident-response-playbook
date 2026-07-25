# Safety Model

## Required controls

- Dedicated lab account before production consideration.
- Explicit resource identifiers; no wildcard discovery followed by mutation.
- Optional `expected_account_id` pinned to the intended account.
- Explicit Region for EC2 and S3 targets.
- `dry_run` defaults to `true` when omitted.
- CloudTrail enabled and CloudWatch log retention configured.
- Human approval for every non-dry-run containment or restoration.
- Incident ID attached to logs and created evidence or quarantine resources.
- Original state captured before reversible containment.
- `confirm_restore: true` and manifest validation before restoration.
- Independent post-action verification.

## Domain safeguards

### EC2

- Quarantine groups must contain no ingress or egress rules.
- Isolation changes every attached network interface, not only the primary interface.
- Original security-group associations are captured per interface.
- A missing security group or interface blocks automated restoration rather than guessing.

### IAM

- The supplied key must belong to the supplied IAM user.
- Current status is checked before mutation.
- Last-used information is collected before disablement.
- Restoration is explicit and should be exceptional.

### S3

- The current caller account is supplied as the expected bucket owner.
- The event Region must match the bucket Region.
- Policy, policy status, ACL, Object Ownership, and Block Public Access are captured before containment.
- Containment changes only bucket-level Block Public Access and leaves policy and ACL unchanged.

## Important limitations

- Security-group replacement can interrupt Systems Manager, monitoring, administrative, and application paths.
- EBS snapshots preserve block-storage state, not memory or every volatile artifact.
- Deactivating one IAM user access key does not revoke already-issued role sessions or unrelated credentials.
- S3 Block Public Access can break intentional public websites or distribution workflows.
- Bucket-level settings are not the complete effective-access picture; account and organization controls may also apply.
- Checksummed manifests are not cryptographically signed authorization records.
- SNS publishing is notification, not durable case management.
