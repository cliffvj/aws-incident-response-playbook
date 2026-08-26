output "instance_id" {
  value       = aws_instance.target.id
  description = "Benign capstone target EC2 instance ID."
}

output "vpc_id" {
  value       = aws_vpc.lab.id
  description = "Capstone VPC ID."
}

output "target_security_group_id" {
  value       = aws_security_group.target.id
  description = "Original target security group restored during rollback."
}

output "event_rule_name" {
  value       = aws_cloudwatch_event_rule.simulated_finding.name
  description = "Lab-only EventBridge rule name."
}

output "target_public_ip" {
  value       = aws_instance.target.public_ip
  description = "Public IPv4 used only for outbound lab connectivity; there are no inbound SG rules."
}
