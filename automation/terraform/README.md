# Terraform Deployment

This Terraform configuration deploys the Phase 3 response-action Lambdas, EC2 Step Functions orchestration, and Phase 3 Commit 4 Systems Manager investigation infrastructure.

> [!WARNING]
> Treat this as a lab reference, not a drop-in production module. Review IAM scopes, evidence retention, approval-channel access, logging, and target-resource boundaries before applying it anywhere outside an isolated account.

## Resources

### Response actions and orchestration

- Eleven response-action Lambda functions and per-action roles
- Per-function CloudWatch Logs groups
- KMS-encrypted incident SNS topic
- KMS-encrypted dedicated approval SNS topic
- Step Functions Standard Workflow for EC2 triage, containment, and rollback
- Step Functions execution role
- DynamoDB execution-correlation / duplicate-event table
- Step Functions CloudWatch Logs group
- Standalone approver callback IAM policy (not attached automatically)
- Optional lab email subscription to the approval topic

### Systems Manager investigation

- Linux read-only evidence-collection Automation document
- Windows read-only evidence-collection Automation document
- Systems Manager Automation execution role
- Versioned S3 evidence bucket with Block Public Access
- Dedicated KMS key with rotation and S3 Bucket Keys enabled
- Configurable current/noncurrent evidence lifecycle retention
- TLS-only evidence-bucket policy
- Managed-node evidence-write policy (**not attached automatically**)
- Responder start/read policy (**not attached automatically**)

## Prerequisites

- Terraform `>= 1.6`
- AWS CLI and authorized lab credentials
- An AWS account/Region containing the authorized test EC2 instance
- A target instance that is `Online` in Systems Manager for SSM investigation testing
- The target's normal Systems Manager managed-node permissions
- Existing S3/IAM lab resources if you also test the independent S3/IAM Lambda actions

## Configure

```bash
cd automation/terraform
cp terraform.tfvars.example terraform.tfvars
```

Review at least:

- `aws_region`
- `s3_bucket_arns`
- `iam_user_arns`
- `approval_timeout_seconds`
- `step_functions_include_execution_data` (recommended `false`)
- `ssm_evidence_bucket_name`
- `ssm_evidence_retention_days`
- `ssm_evidence_noncurrent_retention_days`
- ownership/environment tags

Leave `approval_email_endpoint = null` unless an explicitly authorized lab mailbox should receive callback tokens.

## Validate and deploy

```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan -out=tfplan
terraform show tfplan
terraform apply tfplan
```

Record these outputs:

```bash
terraform output function_names
terraform output state_machine_arn
terraform output approval_topic_arn
terraform output execution_table_name
terraform output approver_policy_arn
terraform output ssm_linux_document_name
terraform output ssm_windows_document_name
terraform output ssm_automation_role_arn
terraform output ssm_evidence_bucket_name
terraform output ssm_evidence_node_policy_arn
terraform output ssm_investigation_operator_policy_arn
```

The approver, managed-node evidence, and SSM investigation operator policies are deliberately not attached. Attach them only to dedicated identities/roles that require those exact capabilities.

## First Step Functions execution

Start with a dry-run:

```bash
cd ../..
STATE_MACHINE_ARN="$(terraform -chdir=automation/terraform output -raw state_machine_arn)"

automation/scripts/start_orchestration.sh \
  "$STATE_MACHINE_ARN" \
  automation/step-functions/samples/containment-dry-run.json
```

Replace all sample account and instance identifiers first. Keep `dry_run` true.

## First Systems Manager investigation

Before starting an SSM investigation:

1. Attach the `ssm_evidence_node_policy_arn` policy to **only** the authorized lab instance role.
2. Verify the node is `Online` in Systems Manager.
3. Give the dedicated responder identity the `ssm_investigation_operator_policy_arn` policy or an equivalent reviewed policy.
4. Start with Linux in a disposable/authorized instance.

From the repository root:

```bash
automation/scripts/start_ssm_investigation.sh \
  linux \
  i-0123456789abcdef0 \
  IR-2026-0001
```

See [Systems Manager evidence collection](../ssm/README.md) for retrieval and integrity verification.

## Live Step Functions approval test

Only after the dry-run output, execution history, permissions, evidence requirements, and rollback path are reviewed:

1. Create a new unique `event_id`.
2. Set `dry_run` to `false` in a local, untracked test event.
3. Start the execution.
4. Confirm evidence snapshots and the waiting approval state.
5. Retrieve the approval message from the dedicated approved endpoint.
6. Resolve it using `automation/scripts/respond_to_approval.sh APPROVE` or `DENY`.

Do not store callback task tokens in files or shell history.

## Cleanup

```bash
terraform destroy
rm -f ./*.zip tfplan response.json
```

Important cleanup behavior:

- Terraform does not delete EBS snapshots created by incident actions.
- Terraform does not undo target-resource changes already performed by response actions.
- A non-empty versioned SSM evidence bucket prevents bucket destruction until evidence is intentionally removed.
- Do not empty evidence solely to make `terraform destroy` succeed; first apply the incident's approved retention and disposition process.

See [Step Functions orchestration](../step-functions/README.md), [Systems Manager investigation](../ssm/README.md), and [cost and cleanup](../docs/cost-and-cleanup.md).
