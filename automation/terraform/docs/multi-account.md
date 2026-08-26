# Multi-account deployment pattern

For AWS Organizations, prefer a split model:

1. **Member-account response plane:** deploy response actions and SSM investigation in each account that may need containment.
2. **Security-account coordination plane:** aggregate selected EventBridge findings for visibility, case creation, and human coordination.
3. **Cross-account execution only by explicit design:** the current Lambda actions fail closed on account mismatch and are not converted into arbitrary cross-account responders by this commit.

The examples under `examples/organizations/` show an organization-scoped event-bus permission and member-account GuardDuty forwarding. They intentionally stop before cross-account remediation.

## Delegated security account

A delegated security account can host Security Hub/GuardDuty administration and event aggregation. Do not assume that delegated administration automatically grants permission to mutate member-account EC2, IAM, S3, or KMS resources. Those permissions require separately reviewed roles and trust policies.

## Permissions boundaries

Set `permissions_boundary_arn` when your organization requires a boundary on Terraform-created execution roles. The boundary must still permit the intended least-privilege actions or deployments/executions will fail.
