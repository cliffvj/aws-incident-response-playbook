output "normalizer_function_name" { value = aws_lambda_function.detection_normalizer.function_name }
output "normalizer_function_arn" { value = aws_lambda_function.detection_normalizer.arn }
output "dlq_url" { value = aws_sqs_queue.detection_dlq.url }
output "dedup_table_name" { value = aws_dynamodb_table.detection_dedup.name }
