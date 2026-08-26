variable "source_root" { type = string }
variable "project_name" { type = string }
variable "role_arns" { type = map(string) }
variable "incident_topic_arn" { type = string }
variable "timeout_seconds" { type = number }
variable "memory_mb" { type = number }
variable "tags" { type = map(string) }
