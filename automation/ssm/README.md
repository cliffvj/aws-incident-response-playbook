# Systems Manager Evidence Collection

Phase 3 Commit 4 adds **read-only, no-SSH/no-RDP host investigation** using AWS Systems Manager Automation and Run Command.

> [!WARNING]
> These runbooks are production-inspired lab references. Host commands can still change access times, populate caches, and affect volatile state. Use them only with authorization and an approved evidence plan. For legal or forensic imaging requirements, use your organization's dedicated forensic procedures.

## What is included

| File | Platform | Purpose |
|---|---|---|
| `collect-linux-evidence.json` | Linux | Process, network, service, package, user, scheduled-task, filesystem-metadata, and selected-log collection |
| `collect-windows-evidence.json` | Windows | Process, network, service, updates/software, user, scheduled-task, and selected-event-log collection |
| `collection-scope.md` | Both | Exact evidence categories, limits, omissions, and platform boundaries |
| `diagrams/ssm-evidence-flow.mmd` | Both | Collection and integrity flow |
| `samples/` | Both | Parameter examples for authorized lab executions |

Terraform deploys the documents with project-specific names rather than an `AWS-` prefix because AWS reserves several document-name prefixes for Amazon-owned documents.

## Safety model

1. **Read-only collection only.** These documents do not quarantine, stop, terminate, patch, delete, or alter security groups.
2. **Managed-node preflight.** Collection aborts when the target is not returned by Systems Manager, is not `Online`, or does not match the expected platform.
3. **No inbound administration port.** The workflow uses Systems Manager; it does not require opening SSH or RDP.
4. **Encrypted evidence destination.** Terraform creates a versioned S3 evidence bucket with default SSE-KMS encryption and Block Public Access.
5. **Unique evidence path.** Output is segmented by incident ID, instance ID, Automation execution ID, and platform.
6. **Integrity metadata.** A post-collection Automation step calculates SHA-256 for every S3 command-output object and writes `integrity-manifest.json`.
7. **Separated roles.** The Automation execution role, managed-node evidence-write policy, and operator evidence-read policy are independent.
8. **No automatic containment.** Host remediation remains outside this commit.

## Evidence path

A typical execution writes under:

```text
s3://<evidence-bucket>/incidents/<incident-id>/<instance-id>/<automation-execution-id>/linux/
```

or:

```text
s3://<evidence-bucket>/incidents/<incident-id>/<instance-id>/<automation-execution-id>/windows/
```

Run Command adds its own command/plugin path beneath that prefix. The finalizer then adds:

```text
integrity-manifest.json
```

The manifest records the incident ID, instance ID, platform, Automation execution ID, Run Command ID, completion timestamp, per-object size/ETag/version/SHA-256, and a canonical evidence-index SHA-256.

## Prerequisites

The target EC2 instance must:

- be registered and **Online** in Systems Manager;
- have a functioning SSM Agent;
- have the normal Systems Manager managed-node permissions (for example, via an approved instance profile); and
- have the generated **SSM evidence node policy** attached to its instance role so Run Command can write to the evidence bucket and use the evidence KMS key.

The operator must have permission to start the deployed Automation document and pass the generated Automation execution role. Terraform creates an operator policy as a reference but does **not** attach it automatically.

## Deploy

```bash
cd automation/terraform
terraform fmt -recursive
terraform init
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```

Record:

```bash
terraform output ssm_linux_document_name
terraform output ssm_windows_document_name
terraform output ssm_evidence_bucket_name
terraform output ssm_automation_role_arn
terraform output ssm_evidence_node_policy_arn
terraform output ssm_investigation_operator_policy_arn
```

Attach the evidence-node policy only to the authorized lab instance role. Do not broadly attach it to fleet roles.

## Start a Linux investigation

From the repository root:

```bash
automation/scripts/start_ssm_investigation.sh \
  linux \
  i-0123456789abcdef0 \
  IR-2026-0001
```

The helper reads Terraform outputs for the document, evidence bucket, and Automation role unless you override them with environment variables. It prints the Automation execution ID and a command to inspect the execution.

## Retrieve and verify

Inspect execution status:

```bash
aws ssm get-automation-execution \
  --automation-execution-id <execution-id>
```

List evidence:

```bash
aws s3 ls \
  s3://<bucket>/incidents/<incident-id>/<instance-id>/<execution-id>/ \
  --recursive
```

Verify every object against the generated manifest:

```bash
python3 automation/scripts/verify_evidence_manifest.py \
  s3://<bucket>/incidents/<incident-id>/<instance-id>/<execution-id>/linux/integrity-manifest.json
```

The verifier performs read-only S3 operations and exits non-zero if an object is missing or its SHA-256 does not match.

## Failure behavior

| Condition | Behavior |
|---|---|
| Instance is not an SSM managed node | Preflight aborts before Run Command |
| SSM Agent is not `Online` | Preflight aborts |
| Wrong OS document chosen | Preflight aborts |
| Instance role cannot write S3/KMS evidence | Run Command fails or evidence output is incomplete; do not treat the execution as complete |
| One collection command is unavailable | The section reports `[not installed]` and collection continues where safe |
| Run Command itself fails | Automation aborts before manifest finalization |
| Manifest hashing/writing fails | Automation fails; retain command output and investigate the incomplete integrity step |

## Platform boundaries

Linux is the primary lab-validation target for this commit. The Windows document is included as a read-only reference and should receive the same account-specific validation before broader use. macOS is intentionally unsupported in this release.

Neither document collects memory, deleted files, full disk images, process environment blocks, browser data, application secrets, or arbitrary user files. See [collection scope](collection-scope.md).

## Cleanup and retention

The Terraform evidence bucket has configurable lifecycle retention. `terraform destroy` attempts to remove infrastructure but **will not empty a non-empty evidence bucket**. This is intentional: incident artifacts should not disappear just because automation infrastructure is destroyed.

Review evidence ownership and retention requirements first, then use an explicit, separately approved deletion process when evidence no longer needs to be retained.

## Related material

- [Scenario 14 — Systems Manager investigation](../../docs/14-systems-manager-investigation.md)
- [Automation safety model](../docs/safety-model.md)
- [IAM permissions matrix](../iam/permissions-matrix.md)
- [Terraform deployment](../terraform/README.md)
- [Cost and cleanup](../docs/cost-and-cleanup.md)
