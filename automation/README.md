# AWS Incident Response Automation

Phase 3 converts the repository's documented response procedures into modular, deployable, testable, and auditable AWS automation.

**Current automation release:** `v2.4.0 — SSM Investigation`

## Capabilities

- Eleven independent, reversible Lambda response actions
- Step Functions EC2 triage, evidence, containment, approval, and rollback orchestration
- Systems Manager read-only Linux and Windows host investigation without opening SSH/RDP
- Versioned SSE-KMS evidence storage with per-object SHA-256 integrity manifests
- Dry-run defaults, rollback manifests, duplicate-event controls, bounded retries, and human approval gates
- Least-privilege IAM examples and Terraform deployment
- Local and CI validation for Python, JSON, action contracts, Step Functions, SSM documents, Lambda packaging, Terraform, and Markdown links

## Safety principles

1. **Dry-run first** for mutating Lambda actions.
2. **Read-only first** for SSM host collection.
3. **Evidence before containment** when incident conditions allow it.
4. **Human approval** before high-impact live containment and rollback in the reference Step Functions workflow.
5. **Unique incident correlation** across Lambda actions, workflow executions, SSM Automation execution IDs, and evidence prefixes.
6. **No blind compensation.** Partial containment failures stop for operator review rather than automatically erasing a desired isolation.
7. **Least privilege.** Each component receives only the permissions needed for its defined role.
8. **Encrypted evidence and notification channels.** Terraform uses customer-managed KMS keys for SSM evidence and incident/approval SNS topics.
9. **No automatic finding trigger yet.** EventBridge/GuardDuty/Security Hub integration remains reserved for Commit 5.
10. **Authorized labs only.** Do not deploy or invoke this repository's automation against production without organization-specific review and approval.

## Directory map

```text
automation/
├── action-catalog.json   # Machine-readable Lambda action inventory
├── lambda/               # Eleven independent response actions
├── step-functions/       # EC2 orchestration ASL, diagrams, samples, operator guide
├── ssm/                  # Read-only host evidence Automation documents, scope, samples
├── shared/               # Validation, manifests, state, logging, context, and tagging
├── iam/                  # Permissions matrix and policy examples
├── terraform/            # Actions, orchestration, encrypted evidence storage, SSM documents
├── samples/              # Action-level dry-run and rollback events
├── tests/                # Mocked unit and structural validation tests
├── scripts/              # Packaging, validation, execution, approval, evidence verification
└── docs/                 # Architecture, operations, rollback, safety, cost, troubleshooting
```

## Recommended path

1. Read the [safety model](docs/safety-model.md).
2. Review [response actions](docs/response-actions.md) and [rollback manifests](docs/rollback-manifests.md).
3. Read the [Step Functions orchestration guide](step-functions/README.md).
4. Read the [Systems Manager evidence guide](ssm/README.md) and [collection scope](ssm/collection-scope.md).
5. Review the [permissions matrix](iam/permissions-matrix.md).
6. Run [testing and validation](tests/README.md).
7. Deploy only to a dedicated lab with [Terraform](terraform/README.md).
8. Start Step Functions with dry-run events and SSM with read-only Linux evidence collection.
9. Verify SSM evidence manifests before relying on collected output.
10. Test rollback planning before any live containment/restoration exercise.

## Authoritative AWS references

- [AWS Systems Manager Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation.html)
- [Systems Manager `aws:runCommand`](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-action-runcommand.html)
- [Systems Manager `aws:executeScript`](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-action-executeScript.html)
- [Running commands on managed nodes](https://docs.aws.amazon.com/systems-manager/latest/userguide/running-commands.html)
- [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Building Lambda functions with Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
