output "lambda_log_group_names" { value = { for k, v in aws_cloudwatch_log_group.lambda : k => v.name } }
output "step_functions_log_group_arn" { value = aws_cloudwatch_log_group.step_functions.arn }
output "detection_normalizer_log_group_name" { value = aws_cloudwatch_log_group.detection_normalizer.name }
output "detection_normalizer_log_group_arn" { value = aws_cloudwatch_log_group.detection_normalizer.arn }
