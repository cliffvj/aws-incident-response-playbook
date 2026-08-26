variable "project_name" {
  type = string
}

variable "tags" {
  type = map(string)
}

variable "approval_email_endpoint" {
  type     = string
  default  = null
  nullable = true
}

variable "kms_deletion_window_days" {
  type    = number
  default = 7
}
