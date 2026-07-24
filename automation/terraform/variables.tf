variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "aws-ir-lab"
}

variable "log_retention_days" {
  type    = number
  default = 30
}

variable "tags" {
  type    = map(string)
  default = {}
}
