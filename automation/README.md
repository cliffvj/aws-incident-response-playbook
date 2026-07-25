# Response Automation Framework

This directory contains production-inspired, lab-safe automation for AWS incident response. The framework is **dry-run first**, modular, auditable, account- and Region-aware, idempotent where practical, and intentionally disconnected from automatic detection triggers until later Phase 3 commits.

> [!WARNING]
> These actions can cause outages, disable identities, change network reachability, create billable evidence artifacts, and interrupt legitimate S3 access. Deploy only in an authorized lab account first. Confirm the caller account, Region, incident ID, target ownership, evidence requirements, approval, and rollback path before setting `dry_run` to `false`.

## Phase 3 Commit 2 scope

Commit 2 expands the initial framework into a complete action catalog with reversible containment paths.

| Action | Purpose | Mutation | Idempotency | Automated rollback |
|---|---|---:|---:|---|
| `collect_ec2_metadata` | Gather instance, network, volume, IAM-profile, and tag metadata | No | Read-only | Not required |
| `ensure_quarantine_security_group` | Create or reuse a per-incident ruleless quarantine group | Yes | Reuses a matching ruleless group | Manual deletion after recovery |
| `isolate_ec2_instance` | Replace security groups on all attached network interfaces | Yes | Skips already isolated interfaces | `restore_ec2_security_groups` |
| `restore_ec2_security_groups` | Restore interface associations from a validated manifest | Yes | Skips already restored interfaces | Re-isolate if required |
| `snapshot_ebs_volumes` | Create tagged evidence snapshots | Yes | Reuses incident/source-volume matches | Retention-controlled deletion |
| `disable_iam_access_key` | Set a verified IAM user key to `Inactive` | Yes | Skips inactive keys | `restore_iam_access_key` |
| `restore_iam_access_key` | Restore the captured key status | Yes | Skips matching status | Disable again if required |
| `inspect_s3_public_access` | Capture Block Public Access, policy, ACL, and ownership state | No | Read-only | Not required |
| `contain_s3_public_access` | Enable all bucket-level Block Public Access controls | Yes | Skips already blocked buckets | `restore_s3_public_access` |
| `restore_s3_public_access` | Restore the captured bucket-level Block Public Access state | Yes | Skips matching state | Re-contain if required |
| `notify_incident` | Publish a structured SNS incident update | Yes | Operator controlled | Follow-up correction only |

The machine-readable [`action-catalog.json`](action-catalog.json) connects every action to its sample events, rollback action, and runbooks.

## Design principles

1. **Dry-run by default.** Every mutating function requires `"dry_run": false` before it calls a write API.
2. **Explicit scope.** Events identify the target resource and may pin the expected AWS account and Region.
3. **Record before change.** Reversible containment actions capture original state in checksummed rollback manifests.
4. **Validate before restore.** Rollback requires `confirm_restore: true` plus matching incident, resource, account, Region, action, and checksum.
5. **Idempotent behavior.** Repeated requests return `no_change` when the requested state already exists.
6. **Small actions.** Each Lambda performs one response action and can be orchestrated by Step Functions later.
7. **Least privilege.** Terraform creates one role per function and standalone policies show action-level scopes.
8. **Structured output.** Functions return JSON-compatible records for CloudWatch Logs, case records, and future orchestration.
9. **No automatic containment triggers yet.** EventBridge and finding normalization are reserved for Commit 5.

## Directory map

```text
automation/
├── action-catalog.json   # Machine-readable action inventory
├── lambda/               # Lambda source and per-action guides
├── shared/               # Validation, manifests, S3 state, logging, context, and tagging
├── iam/                  # Permissions matrix and policy examples
├── terraform/            # Deployable lab scaffold
├── samples/              # Dry-run and rollback event examples
├── tests/                # Unit tests with mocked AWS clients
├── scripts/              # Packaging and contract-validation tools
└── docs/                 # Architecture, operations, rollback, safety, cost, and troubleshooting
```

## Recommended path

1. Read the [safety model](docs/safety-model.md).
2. Review the [event contract](docs/event-contract.md) and [rollback manifests](docs/rollback-manifests.md).
3. Inspect the [response action catalog](docs/response-actions.md) and [permissions matrix](iam/permissions-matrix.md).
4. Run local validation using [tests/README.md](tests/README.md).
5. Deploy into a dedicated lab using [terraform/README.md](terraform/README.md).
6. Invoke only sample events with `dry_run: true`.
7. Record the returned plan and rollback manifest before authorizing a write.
8. Perform a controlled non-dry-run test.
9. Verify CloudTrail, CloudWatch Logs, resource state, and rollback behavior.

## Authoritative AWS references

- [Building Lambda functions with Python](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
- [S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
- [S3 `GetPublicAccessBlock`](https://docs.aws.amazon.com/AmazonS3/latest/API/API_GetPublicAccessBlock.html)
- [S3 `PutPublicAccessBlock`](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutPublicAccessBlock.html)
- [Change EC2 security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/changing-security-group.html)
- [EC2 `CreateSecurityGroup`](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateSecurityGroup.html)
- [IAM `ListAccessKeys`](https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListAccessKeys.html)
- [IAM `UpdateAccessKey`](https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateAccessKey.html)
