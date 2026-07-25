# Terraform Deployment Scaffold

This directory deploys one execution role, CloudWatch log group, and Lambda function per response action, plus a KMS-encrypted SNS incident topic.

> [!WARNING]
> The Terraform is a controlled lab scaffold, not a turnkey production deployment. Review generated IAM policies, replace all placeholder resource scopes, run a plan, and test only with `dry_run: true` before authorizing changes.

## Prerequisites

- Terraform `>= 1.6`
- AWS provider credentials for an authorized lab account
- AWS CLI configured for the same account and Region
- An existing general-purpose S3 lab bucket when testing S3 actions
- A dedicated IAM lab user path when testing access-key actions

## Configure

```bash
cd automation/terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit at least:

- `aws_region`
- `s3_bucket_arns`
- `iam_user_arns`
- ownership and environment tags

When `s3_bucket_arns` is empty, Terraform uses an intentionally non-production placeholder bucket ARN. When `iam_user_arns` is empty, it limits IAM actions to the `incident-lab/*` path in the current account. Live tests will fail until these scopes match authorized lab resources.

## Validate and deploy

```bash
terraform fmt -recursive
terraform init
terraform validate
terraform plan -out=tfplan
terraform show tfplan
terraform apply tfplan
```

Record the `function_names`, `function_arns`, `incident_topic_arn`, and effective IAM scopes in the lab change record.

## First invocation

Use a sample event and keep `dry_run` set to `true`:

```bash
aws lambda invoke \
  --function-name aws-ir-lab-contain-s3-public-access \
  --cli-binary-format raw-in-base64-out \
  --payload fileb://../samples/contain-s3-public-access-dry-run.json \
  response.json

cat response.json
```

The sample identifiers are placeholders. Replace them with authorized resources and keep the account and Region checks enabled.

## Cleanup

```bash
terraform destroy
rm -f ./*.zip tfplan response.json
```

Terraform does not manage snapshots created by the response action, quarantine groups retained for rollback, or changes made to target resources. Follow [cost and cleanup guidance](../docs/cost-and-cleanup.md) before destroying the deployment.
