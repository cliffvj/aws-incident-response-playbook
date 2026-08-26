output "state_machine_arn" { value = aws_sfn_state_machine.ec2_incident_response.arn }
output "state_machine_name" { value = aws_sfn_state_machine.ec2_incident_response.name }
output "execution_table_name" { value = aws_dynamodb_table.executions.name }
