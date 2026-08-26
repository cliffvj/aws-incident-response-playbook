variable "aws_region" {
  type        = string
  description = "AWS Region for the authorized capstone lab."
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Name prefix for capstone target resources."
  default     = "aws-ir-capstone"
}

variable "instance_type" {
  type        = string
  description = "Small EC2 instance type for the benign target."
  default     = "t3.micro"
}

variable "detection_normalizer_function_name" {
  type        = string
  description = "Existing Phase 3 detection-normalizer Lambda function name."
}

variable "ssm_evidence_node_policy_arn" {
  type        = string
  description = "Existing Phase 3 managed-node evidence-write policy ARN."
}

variable "tags" {
  type        = map(string)
  description = "Additional tags for target-lab resources."
  default     = {}
}
