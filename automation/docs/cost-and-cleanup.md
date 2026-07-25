# Cost and Cleanup

Potential costs include Lambda invocation and duration, CloudWatch Logs ingestion and retention, EBS snapshot storage, SNS delivery, KMS requests, and any remote Terraform state infrastructure configured by the operator.

The security groups and S3 API configuration changes themselves are not the primary cost drivers, but they can create operational impact that is more significant than direct service charges.

## Cleanup order

1. Export required Lambda logs, CloudTrail records, action results, and rollback manifests.
2. Confirm the incident-retention decision for EBS snapshots.
3. Restore or deliberately retain target-resource changes.
4. Verify that quarantine security groups are unused before deletion.
5. Destroy Terraform-managed Lambda, IAM, log, SNS, and KMS resources.
6. Remove local ZIP archives and Terraform plan files.
7. Review retained CloudWatch log groups, KMS keys pending deletion, snapshots, and manual resource changes.

Terraform does not delete snapshots created by the response Lambda, remove quarantine groups created at runtime, or reverse changes made to EC2, IAM, or S3 targets. Those are operational incident artifacts and must be handled under explicit recovery and evidence-retention decisions.
