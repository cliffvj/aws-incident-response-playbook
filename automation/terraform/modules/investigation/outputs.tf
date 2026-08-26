output "linux_document_name" { value = aws_ssm_document.collect_linux_evidence.name }
output "windows_document_name" { value = aws_ssm_document.collect_windows_evidence.name }
output "automation_role_arn" { value = aws_iam_role.ssm_automation.arn }
output "evidence_bucket_name" { value = aws_s3_bucket.ssm_evidence.bucket }
output "evidence_kms_key_arn" { value = aws_kms_key.ssm_evidence.arn }
output "evidence_node_policy_arn" { value = aws_iam_policy.ssm_evidence_node.arn }
output "operator_policy_arn" { value = aws_iam_policy.ssm_investigation_operator.arn }
