# `contain_s3_public_access` — Contain S3 public access

## Purpose

Capture the bucket public-access state, preserve the policy and ACL unchanged, and enable all four bucket-level S3 Block Public Access settings.

## Invocation contract

- **Required fields:** `incident_id`, `bucket_name`, `region`; recommended: `expected_account_id`, `requested_by`, `reason`.
- **Mutation:** Yes. Block Public Access is changed only when `dry_run` is exactly `false`.
- **Sample event:** [`contain-s3-public-access-dry-run.json`](../../samples/contain-s3-public-access-dry-run.json)
- **IAM example:** [`contain-s3-public-access-policy.json`](../../iam/policies/contain-s3-public-access-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`planned`, `completed`, or `no_change` when all four bucket-level controls are already enabled.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. The expected bucket owner must match the current caller account.
2. The supplied Region must match the bucket Region.
3. The original policy, ACL, policy status, Object Ownership, and Block Public Access configuration are captured before mutation.
4. This containment can interrupt legitimate public website or data-delivery use cases.

## Rollback

The response includes a checksummed manifest containing the full observed state. `restore_s3_public_access` restores only the bucket-level Block Public Access configuration because this action deliberately does not mutate the policy or ACL.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [Public S3 bucket](../../../docs/05-public-s3-bucket.md)
- [S3 data-leak response](../../../docs/s3-data-leak-response.md)
