# Terraform deployment

`v2.6.0 — Deployment Modules` converts the Phase 3 Terraform scaffold into reusable service modules plus an opinionated `platform` composition module.

## Module map

- `modules/notifications` — KMS + SNS
- `modules/logging` — CloudWatch log groups
- `modules/iam` — response, orchestration, and detection execution roles
- `modules/response-actions` — eleven Lambda actions
- `modules/orchestration` — Step Functions + execution correlation
- `modules/investigation` — SSM evidence plane
- `modules/event-routing` — EventBridge normalization, dedupe, DLQ, optional archive
- `modules/platform` — supported reference composition

## First-time lab deployment

```bash
cp terraform.tfvars.example terraform.tfvars
terraform fmt -recursive
terraform init
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```

Replace placeholder S3/IAM scopes before live action testing. The default configuration is still designed for an isolated lab.

## Upgrade from v2.5.0

Read [`docs/state-management.md`](docs/state-management.md) before applying. The included `moved.tf` prevents known root resources from being treated as unrelated module resources, but you must still review the complete plan.

## Environment examples

- [`examples/lab`](examples/lab/)
- [`examples/development`](examples/development/)
- [`examples/controlled-production`](examples/controlled-production/)
- [`examples/organizations`](examples/organizations/)

“Controlled production” is an adaptation template, not production approval. Organizations must supply their own controls, network design, permissions boundaries, state backend, retention policy, testing, change control, and incident authority.
