# Terraform Deployment

This Terraform configuration deploys the Phase 3 response-action Lambdas **and** the Phase 3 Commit 3 EC2 incident-response Step Functions orchestration.

> [!WARNING]
> Treat this as a lab reference, not a drop-in production module. Review IAM scopes, approval-channel access, logging, retention, and target-resource boundaries before applying it anywhere outside an isolated account.

## Resources

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

## Prerequisites

- Terraform `>= 1.6`
- AWS CLI and authorized lab credentials
- An AWS account/Region where the target EC2 test instance exists
- Existing S3/IAM lab resources if you also test those independent actions

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
- ownership/environment tags

Leave `approval_email_endpoint = null` unless an explicitly authorized lab mailbox should receive callback tokens. Email subscription requires confirmation after apply.

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
```

The approver policy is deliberately not attached. Attach it only to the dedicated identity your lab uses to resolve callback tokens.

## First orchestration execution

Start with a dry-run:

```bash
cd ../..
STATE_MACHINE_ARN="$(terraform -chdir=automation/terraform output -raw state_machine_arn)"

automation/scripts/start_orchestration.sh \
  "$STATE_MACHINE_ARN" \
  automation/step-functions/samples/containment-dry-run.json
```

Replace all sample account and instance identifiers first. Keep `dry_run` true.

## Live approval test

Only after the dry-run output, execution history, permissions, evidence requirements, and rollback path are reviewed:

1. Create a new unique `event_id`.
2. Set `dry_run` to `false` in a local, untracked test event.
3. Start the execution.
4. Confirm evidence snapshots and the waiting approval state.
5. Retrieve the approval message from the dedicated approved endpoint.
6. Resolve it using:

```bash
automation/scripts/respond_to_approval.sh APPROVE
```

Use `DENY` when containment is not authorized. Do not store task tokens in files or shell history.

## Cleanup

```bash
terraform destroy
rm -f ./*.zip tfplan response.json
```

Terraform does not delete EBS snapshots created by incident actions or undo changes applied to target resources before destroy. Restore resource state intentionally and apply retention policy to evidence before tearing down orchestration infrastructure.

See [Step Functions orchestration](../step-functions/README.md) and [cost and cleanup](../docs/cost-and-cleanup.md).
