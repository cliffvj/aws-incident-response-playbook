# Terraform Deployment

This scaffold deploys five Lambda functions, separate execution roles, CloudWatch log groups, a customer-managed KMS key, and an encrypted SNS topic. It does **not** create EventBridge rules or automatic containment triggers.

```bash
cd automation/terraform
terraform init
terraform fmt -check
terraform validate
terraform plan -var='project_name=aws-ir-lab'
terraform apply -var='project_name=aws-ir-lab'
```

After deployment, invoke only dry-run sample events first. Terraform builds ZIP archives using `archive_file` from function and shared source files.

Cleanup:

```bash
terraform destroy -var='project_name=aws-ir-lab'
```

Snapshots created by the automation are not Terraform-managed and require separate evidence-approved cleanup.
