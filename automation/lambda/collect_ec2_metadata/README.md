# `collect_ec2_metadata` — Collect EC2 metadata

## Purpose

Collect instance, network-interface, security-group, volume, instance-profile, tag, and lifecycle metadata without changing the workload.

## Invocation contract

- **Required fields:** `incident_id`, `instance_id`; recommended: `expected_account_id`, `region`, `requested_by`.
- **Mutation:** No. The response always reports `dry_run: true` and `status: observed`.
- **Sample event:** [`collect-ec2-metadata.json`](../../samples/collect-ec2-metadata.json)
- **IAM example:** [`collect-ec2-metadata-policy.json`](../../iam/policies/collect-ec2-metadata-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`observed` after successful collection.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. The target instance must exist in the selected account and Region.
2. An optional expected account ID is compared with the Lambda caller account.
3. The response may contain sensitive infrastructure metadata and should be retained with the incident record.

## Rollback

None. This action is read-only.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [EC2 instance compromise](../../../docs/01-ec2-instance-compromise.md)
