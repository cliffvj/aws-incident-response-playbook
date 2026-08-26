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

variable "s3_bucket_arns" {
  type = list(string)
}

variable "iam_user_arns" {
  type = list(string)
}

variable "incident_topic_arn" {
  type = string
}

variable "notification_kms_key_arn" {
  type = string
}

variable "approval_topic_arn" {
  type = string
}

variable "permissions_boundary_arn" {
  type     = string
  default  = null
  nullable = true
}

variable "tags" {
  type = map(string)
}
