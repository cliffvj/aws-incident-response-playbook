# Response Automation Framework

This directory contains production-inspired, lab-safe automation for AWS incident response. The framework is intentionally **dry-run first**, modular, auditable, and disconnected from automatic triggers until each action has been reviewed in an authorized AWS account.

> [!WARNING]
> Automation can cause outages, disable identities, alter network reachability, and create billable resources. Deploy only in an authorized lab account first. Confirm account, Region, incident ID, resource ownership, evidence requirements, and rollback steps before setting `dry_run` to `false`.

## Commit 1 scope

| Component | Purpose | Mutation |
|---|---|---|
| `collect_ec2_metadata` | Gather instance, network, volume, IAM-profile, and tag metadata | None |
| `isolate_ec2_instance` | Replace an instance's security groups with a pre-created quarantine security group | Yes |
| `snapshot_ebs_volumes` | Create tagged snapshots of attached EBS volumes | Yes |
| `disable_iam_access_key` | Set an IAM user access key to `Inactive` | Yes |
| `notify_incident` | Publish a structured incident update to SNS | Yes |

## Design principles

1. **Dry-run by default.** Every mutating function requires `"dry_run": false` before it calls a write API.
2. **Explicit scope.** Events must include the affected resource identifiers and an `incident_id`.
3. **Record before change.** Responses include the observed state needed to plan rollback.
4. **Small actions.** Each Lambda performs one response action and can later be orchestrated by Step Functions.
5. **Least privilege.** IAM examples are split by action rather than combined into one administrator policy.
6. **Structured output.** Functions return JSON-compatible records for CloudWatch Logs and future orchestration.
7. **No automatic triggers yet.** This commit avoids connecting detections directly to containment.

## Directory map

```text
automation/
├── lambda/       # Lambda source and per-action guides
├── shared/       # Validation, logging, response, context, and tagging helpers
├── iam/          # Permissions matrix and policy examples
├── terraform/    # Deployable infrastructure scaffold
├── samples/      # Safe dry-run invocation payloads
├── tests/        # Unit tests with mocked AWS clients
├── scripts/      # Package and validation helpers
└── docs/         # Architecture, event contract, operations, cost, and troubleshooting
```

## Recommended path

1. Read [Safety model](docs/safety-model.md).
2. Review the [event contract](docs/event-contract.md).
3. Inspect the [permissions matrix](iam/permissions-matrix.md).
4. Run local tests using [tests/README.md](tests/README.md).
5. Deploy into a dedicated lab using [terraform/README.md](terraform/README.md).
6. Invoke only sample events with `dry_run: true`.
7. Approve and document a controlled non-dry-run test.
8. Verify CloudTrail, CloudWatch Logs, resource state, and rollback data.

## Authoritative AWS references

- [Building Lambda functions with Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
- [Python Lambda handler](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)
- [Change EC2 security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/changing-security-group.html)
- [IAM UpdateAccessKey API](https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateAccessKey.html)
- [Amazon EventBridge overview](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
