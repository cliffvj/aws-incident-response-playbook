# `inspect_s3_public_access` — Inspect S3 public-access state

## Purpose

Capture bucket-level Block Public Access, policy, policy-status, ACL, and Object Ownership information without modifying the bucket.

## Invocation contract

- **Required fields:** `incident_id`, `bucket_name`, `region`; recommended: `expected_account_id`, `requested_by`.
- **Mutation:** No. The response always reports `dry_run: true` and `status: observed`.
- **Sample event:** [`inspect-s3-public-access.json`](../../samples/inspect-s3-public-access.json)
- **IAM example:** [`inspect-s3-public-access-policy.json`](../../iam/policies/inspect-s3-public-access-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`observed` after the complete state is collected.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. The expected bucket owner is set to the current caller account.
2. The supplied Region must match the bucket Region.
3. Bucket-level settings are evidence, but effective public access can also depend on account-level and organization-level controls.

## Rollback

None. This action is read-only.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [Public S3 bucket](../../../docs/05-public-s3-bucket.md)
- [S3 data-leak response](../../../docs/s3-data-leak-response.md)
