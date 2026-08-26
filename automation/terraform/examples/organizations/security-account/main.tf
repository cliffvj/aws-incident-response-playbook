terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 7.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "organization_id" {
  type = string
}

variable "event_bus_name" {
  type    = string
  default = "aws-ir-security"
}

resource "aws_cloudwatch_event_bus" "security" {
  name = var.event_bus_name
}

resource "aws_cloudwatch_event_bus_policy" "organization" {
  event_bus_name = aws_cloudwatch_event_bus.security.name
  statement_id   = "AllowOrganizationPutEvents"
  action         = "events:PutEvents"
  principal      = "*"

  condition {
    type  = "StringEquals"
    key   = "aws:PrincipalOrgID"
    value = var.organization_id
  }
}

output "event_bus_arn" {
  value = aws_cloudwatch_event_bus.security.arn
}
