# `isolate_ec2_instance` — Isolate an EC2 instance

## Purpose

Replace the security groups on every network interface attached to the target instance with a reviewed, ruleless quarantine security group.

## Invocation contract

- **Required fields:** `incident_id`, `instance_id`, `quarantine_security_group_id`; recommended: `expected_account_id`, `region`, `requested_by`, `reason`.
- **Mutation:** Yes. Interface changes occur only when `dry_run` is exactly `false`.
- **Sample event:** [`isolate-ec2-dry-run.json`](../../samples/isolate-ec2-dry-run.json)
- **IAM example:** [`isolate-ec2-policy.json`](../../iam/policies/isolate-ec2-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`planned`, `completed`, or `no_change` when every interface already uses only the quarantine group.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. The quarantine group must be in the same VPC as the instance.
2. The quarantine group must have no ingress or egress rules.
3. All attached network interfaces are evaluated independently to preserve exact rollback data.
4. Isolation can interrupt Systems Manager, monitoring, application, and administrative paths.

## Rollback

The response includes a checksummed rollback manifest containing the original security-group IDs for each network interface. Pass that exact manifest to `restore_ec2_security_groups` with `confirm_restore: true`.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [Automated EC2 isolation](../../../docs/02-automated-ec2-isolation.md)
