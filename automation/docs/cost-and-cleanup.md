# Cost and Cleanup

Potential costs include Lambda invocations and duration, CloudWatch Logs ingestion and retention, EBS snapshots, SNS notifications, KMS requests, and Terraform state storage if a remote backend is configured.

Cleanup order:

1. Export required logs and action results.
2. Confirm snapshots may be deleted under evidence-retention policy.
3. Destroy Terraform-managed resources.
4. Remove local build archives.
5. Review CloudWatch log groups and retained KMS keys.

Terraform does not delete snapshots created by the response Lambda because they are operational evidence, not resources managed by the deployment stack.
