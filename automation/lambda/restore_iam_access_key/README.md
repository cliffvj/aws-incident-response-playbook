# `restore_iam_access_key` — Restore an IAM user access-key status

## Purpose

Restore an IAM user access key to the status captured before `disable_iam_access_key`.

## Invocation contract

- **Required fields:** `incident_id`, `user_name`, `access_key_id`, `rollback_manifest`, `confirm_restore`; recommended: `expected_account_id`, `requested_by`, `reason`.
- **Mutation:** Yes. Restoration requires `confirm_restore: true` and `dry_run: false`.
- **Sample event:** [`restore-iam-key-dry-run.json`](../../samples/restore-iam-key-dry-run.json)
- **IAM example:** [`restore-iam-key-policy.json`](../../iam/policies/restore-iam-key-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`planned`, `completed`, or `no_change` when the current key status already equals the captured status.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. Manifest checksum, incident ID, resource ID, user name, and account must match.
2. Re-enabling a compromised key is normally inappropriate; prefer replacement and deletion when operationally possible.
3. The action accepts only `Active` or `Inactive` as a captured target state.

## Rollback

This is the rollback action. Re-disabling the key remains available through `disable_iam_access_key` if recovery validation fails.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [IAM credential compromise](../../../docs/03-iam-credential-compromise.md)
