variable "source_root" {
  type = string
}

variable "project_name" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "account_id" {
  type = string
}

variable "partition" {
  type = string
}

variable "bucket_name" {
  type     = string
  default  = null
  nullable = true
}

variable "retention_days" {
  type = number
}

variable "noncurrent_retention_days" {
  type = number
}

variable "permissions_boundary_arn" {
  type     = string
  default  = null
  nullable = true
}

variable "kms_deletion_window_days" {
  type    = number
  default = 7
}

variable "tags" {
  type = map(string)
}
