output "lambda_role_arns" { value = { for k, v in aws_iam_role.lambda : k => v.arn } }
output "step_functions_role_arn" { value = aws_iam_role.step_functions.arn }
output "approver_policy_arn" { value = aws_iam_policy.step_functions_approver.arn }
output "detection_normalizer_role_arn" { value = aws_iam_role.detection_normalizer.arn }
