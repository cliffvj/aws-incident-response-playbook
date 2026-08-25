# Response Automation Framework

This directory contains production-inspired, lab-safe AWS incident-response automation. The framework is **dry-run first**, modular, auditable, account- and Region-aware, reversible where practical, and now includes a controlled AWS Step Functions orchestration layer.

> [!WARNING]
> These actions can cause outages, disable identities, change network reachability, create billable evidence artifacts, and interrupt legitimate S3 access. Deploy only in an authorized lab first. Confirm account, Region, incident ID, target ownership, evidence requirements, approval, and rollback before live execution.

## Phase 3 Commit 3 scope

Commit 3 keeps all eleven `v2.2.0` response actions and adds a reference **EC2 incident-response Standard Workflow** that coordinates selected actions.

| Capability | Commit 3 behavior |
|---|---|
| Triage | Read EC2 metadata and produce a structured notification path |
| Evidence | Snapshot attached EBS volumes before live network containment |
| Containment | Prepare/reuse a ruleless quarantine SG and isolate all instance ENIs |
| Approval | Pause live containment and live rollback with SNS `waitForTaskToken` callbacks |
| Rollback | Validate a checksummed isolation manifest, plan restoration, then restore only after approval |
| Deduplication | Reject repeated `event_id` values through a DynamoDB conditional write |
| Failure handling | Bounded Lambda retries, catches, approval timeouts, failure records, and explicit partial-failure states |
| Auditability | Step Functions execution history plus DynamoDB execution correlation and CloudWatch Logs |

Machine-readable inventories are available in [`action-catalog.json`](action-catalog.json) and [`orchestration-catalog.json`](orchestration-catalog.json).

## Design principles

1. **Dry-run by default.** Missing orchestration `dry_run` becomes `true`; mutating Lambda actions also default to dry-run.
2. **Evidence before high-impact containment.** Live containment preserves EBS evidence before requesting network-isolation approval.
3. **Human approval boundaries.** Live containment and live rollback use a dedicated approval SNS topic and callback task token.
4. **Separate sensitive channels.** Approval task tokens never go to the general incident-notification topic.
5. **Explicit scope.** Events identify incident, event, account, Region, target resource, requester, and reason.
6. **Validated rollback.** Restore actions require `confirm_restore: true` plus a matching checksummed manifest.
7. **Duplicate suppression.** `event_id` is a one-time orchestration key; `incident_id` correlates multiple distinct response events.
8. **No blind compensation.** Partial containment failures stop for operator review instead of automatically reversing a potentially desired isolation.
9. **Least privilege.** Step Functions gets only the response-action invocation, approval-topic, execution-table, KMS, and log-delivery permissions it needs.
10. **No automatic finding trigger yet.** EventBridge/GuardDuty/Security Hub integration remains reserved for Commit 5.

## Directory map

```text
automation/
├── action-catalog.json   # Machine-readable action inventory
├── lambda/               # Eleven independent response actions
├── step-functions/       # EC2 orchestration ASL, diagrams, samples, operator guide
├── shared/               # Validation, manifests, state, logging, context, and tagging
├── iam/                  # Permissions matrix and policy examples
├── terraform/            # Actions plus orchestration deployment
├── samples/              # Action-level dry-run and rollback events
├── tests/                # Mocked unit tests and orchestration structural tests
├── scripts/              # Packaging, validation, execution, and approval helpers
└── docs/                 # Architecture, operations, rollback, safety, cost, troubleshooting
```

## Recommended path

1. Read the [safety model](docs/safety-model.md).
2. Review [response actions](docs/response-actions.md) and [rollback manifests](docs/rollback-manifests.md).
3. Read the [Step Functions orchestration guide](step-functions/README.md).
4. Review the [permissions matrix](iam/permissions-matrix.md).
5. Run [testing and validation](tests/README.md).
6. Deploy to a dedicated lab with [Terraform](terraform/README.md).
7. Start with `triage-dry-run.json` and `containment-dry-run.json`.
8. Inspect execution history and DynamoDB correlation records before attempting a live approval path.
9. Test a rollback plan before performing a live restoration.

## Authoritative AWS references

- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Step Functions Lambda integration](https://docs.aws.amazon.com/step-functions/latest/dg/connect-lambda.html)
- [Step Functions callback task token pattern](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token)
- [Step Functions error handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)
- [Building Lambda functions with Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
- [Change EC2 security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/changing-security-group.html)
