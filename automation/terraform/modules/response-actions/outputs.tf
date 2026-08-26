output "function_names" { value = { for k, v in aws_lambda_function.action : k => v.function_name } }
output "function_arns" { value = { for k, v in aws_lambda_function.action : k => v.arn } }
