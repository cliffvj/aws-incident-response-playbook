# `restore_ec2_security_groups` — Restore EC2 security groups

## Purpose

Restore network-interface security-group associations from a validated rollback manifest produced by `isolate_ec2_instance`.

## Invocation contract

- **Required fields:** `incident_id`, `instance_id`, `rollback_manifest`, `confirm_restore`; recommended: `expected_account_id`, `region`, `requested_by`, `reason`.
- **Mutation:** Yes. Restoration requires `confirm_restore: true` and `dry_run: false`.
- **Sample event:** [`restore-ec2-security-groups-dry-run.json`](../../samples/restore-ec2-security-groups-dry-run.json)
- **IAM example:** [`restore-ec2-security-groups-policy.json`](../../iam/policies/restore-ec2-security-groups-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`planned`, `completed`, or `no_change` when every interface already matches the captured state.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. Manifest checksum, action, incident ID, resource ID, account, and Region must match.
2. Every referenced network interface must still exist.
3. The function restores only the associations captured before isolation; it does not recreate deleted security groups.

## Rollback

This is the rollback action. Preserve the current quarantine state separately before executing if a second reversal may be required.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [Automated EC2 isolation](../../../docs/02-automated-ec2-isolation.md)
