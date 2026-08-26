variable "project_name" { type = string }
variable "action_names" { type = set(string) }
variable "retention_in_days" { type = number }
variable "tags" { type = map(string) }
