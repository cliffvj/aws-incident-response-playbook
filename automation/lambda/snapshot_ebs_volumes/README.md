# `snapshot_ebs_volumes` — Snapshot attached EBS volumes

## Purpose

Create incident-tagged snapshots for EBS volumes attached to a target instance while preventing duplicate snapshots for the same incident and source volume.

## Invocation contract

- **Required fields:** `incident_id`, `instance_id`; recommended: `expected_account_id`, `region`, `requested_by`, `reason`.
- **Mutation:** Yes. Snapshot creation occurs only when `dry_run` is exactly `false`.
- **Sample event:** [`snapshot-ebs-dry-run.json`](../../samples/snapshot-ebs-dry-run.json)
- **IAM example:** [`snapshot-ebs-policy.json`](../../iam/policies/snapshot-ebs-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`planned`, `submitted`, or `no_change` when a non-error snapshot already exists for every incident/source-volume pair.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. The function records source instance and volume IDs as tags.
2. Snapshot completion is asynchronous; `submitted` does not mean the snapshot is complete.
3. EBS snapshots do not capture memory or all volatile host state.

## Rollback

Snapshots are evidence artifacts. Delete them only under the documented evidence-retention and case-closure process; deletion is intentionally not automated.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [EBS snapshot forensic preservation](../../../docs/19-ebs-snapshot-forensic-preservation.md)
