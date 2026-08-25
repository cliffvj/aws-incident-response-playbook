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
- SNS publishing is notification, not durable case management.\n## Orchestration approval safety\n\nCommit 3 introduces a dedicated approval SNS topic. Callback task tokens are sensitive authorization material. Keep execution-data logging disabled by default, distribute tokens only to a dedicated approval endpoint, and attach callback permissions only to a strongly authenticated approver identity. Live containment and live rollback must not bypass their approval states.\n

## SSM evidence-collection safeguards

- Host investigation is separated from host containment/remediation.
- Linux and Windows runbooks abort when the node is unmanaged/offline or the expected platform does not match.
- Collection uses bounded output and selected logs rather than unrestricted recursive file capture.
- Evidence identifiers must not contain secrets.
- Run Command output is written to a versioned SSE-KMS S3 bucket and finalized with per-object SHA-256 values.
- The generated managed-node write policy and responder read policy are not attached automatically.
- SSM evidence output can contain sensitive process arguments, scheduled commands, and log content; access it as incident evidence.
