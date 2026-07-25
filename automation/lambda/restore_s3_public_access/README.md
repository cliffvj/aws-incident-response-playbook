# `restore_s3_public_access` — Restore S3 Block Public Access

## Purpose

Restore the bucket-level S3 Block Public Access state captured by `contain_s3_public_access`.

## Invocation contract

- **Required fields:** `incident_id`, `bucket_name`, `region`, `rollback_manifest`, `confirm_restore`; recommended: `expected_account_id`, `requested_by`, `reason`.
- **Mutation:** Yes. Restoration requires `confirm_restore: true` and `dry_run: false`.
- **Sample event:** [`restore-s3-public-access-dry-run.json`](../../samples/restore-s3-public-access-dry-run.json)
- **IAM example:** [`restore-s3-public-access-policy.json`](../../iam/policies/restore-s3-public-access-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`planned`, `completed`, or `no_change` when the bucket already matches the captured state.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. Manifest checksum, incident ID, bucket name, account, and Region must match.
2. When no bucket-level configuration existed originally, restoration deletes the containment configuration.
3. The action does not restore or alter policy and ACL documents because containment did not change them.

## Rollback

This is the rollback action. Re-run `contain_s3_public_access` if restored access is found to be unsafe.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [Public S3 bucket](../../../docs/05-public-s3-bucket.md)
