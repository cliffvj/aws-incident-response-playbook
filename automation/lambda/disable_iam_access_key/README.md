# `disable_iam_access_key` — Disable an IAM user access key

## Purpose

Verify that an access key belongs to the supplied IAM user and set its status to `Inactive` after dry-run review.

## Invocation contract

- **Required fields:** `incident_id`, `user_name`, `access_key_id`; recommended: `expected_account_id`, `requested_by`, `reason`.
- **Mutation:** Yes. The key is updated only when `dry_run` is exactly `false`.
- **Sample event:** [`disable-iam-key-dry-run.json`](../../samples/disable-iam-key-dry-run.json)
- **IAM example:** [`disable-iam-key-policy.json`](../../iam/policies/disable-iam-key-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`planned`, `completed`, or `no_change` when the key is already inactive.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. The key ID must appear in `ListAccessKeys` for the supplied IAM user.
2. Last-used information is collected before containment.
3. Disabling one long-term access key does not revoke role sessions or unrelated credentials.

## Rollback

The response contains a rollback manifest with the original key status. Use `restore_iam_access_key` only after investigation, credential rotation, and explicit authorization.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [IAM credential compromise](../../../docs/03-iam-credential-compromise.md)
