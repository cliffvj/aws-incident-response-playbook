# `ensure_quarantine_security_group` — Ensure quarantine security group

## Purpose

Create or reuse a per-incident, ruleless VPC security group that can be supplied to the EC2 isolation action.

## Invocation contract

- **Required fields:** `incident_id`, `vpc_id`; recommended: `expected_account_id`, `region`, `requested_by`, `reason`.
- **Mutation:** Yes. Creation occurs only when `dry_run` is exactly `false`.
- **Sample event:** [`ensure-quarantine-sg-dry-run.json`](../../samples/ensure-quarantine-sg-dry-run.json)
- **IAM example:** [`ensure-quarantine-security-group-policy.json`](../../iam/policies/ensure-quarantine-security-group-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`planned` when creation is needed in dry-run, `completed` after creation and rule removal, or `no_change` when a matching ruleless group already exists.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. The generated name is scoped to the incident ID.
2. Existing groups are reused only when both ingress and egress rule lists are empty.
3. The default outbound rule on a newly created security group is revoked before success is returned.

## Rollback

Delete the security group manually only after every interface has been restored and the group is unused. Deletion is intentionally not automated in this commit.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [Automated EC2 isolation](../../../docs/02-automated-ec2-isolation.md)
- [Security group open to the world](../../../docs/16-security-group-open-to-world.md)
