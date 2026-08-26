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
variable "role_arn" {
  type = string
}
variable "state_machine_arn" {
  type = string
}
variable "incident_topic_arn" {
  type = string
}
variable "log_group_name" {
  type = string
}
variable "default_route" {
  type = string
}
variable "allowed_account_ids" {
  type = list(string)
}
variable "ignore_principal_arn_prefixes" {
  type = list(string)
}
variable "dedup_ttl_seconds" {
  type = number
}
variable "dlq_retention_seconds" {
  type = number
}
variable "max_event_age_seconds" {
  type = number
}
variable "max_retry_attempts" {
  type = number
}
variable "enable_event_archive" {
  type = bool
}
variable "archive_retention_days" {
  type = number
}
variable "enable_cloudwatch_alarm_routing" {
  type = bool
}
variable "cloudwatch_security_log_group_name" {
  type     = string
  default  = null
  nullable = true
}
variable "tags" {
  type = map(string)
}
