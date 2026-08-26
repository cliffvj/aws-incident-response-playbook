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

variable "security_event_bus_arn" {
  type = string
}

resource "aws_iam_role" "event_forwarder" {
  name = "aws-ir-event-forwarder"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "events.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "event_forwarder" {
  name = "aws-ir-event-forwarder"
  role = aws_iam_role.event_forwarder.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["events:PutEvents"]
      Resource = var.security_event_bus_arn
    }]
  })
}

resource "aws_cloudwatch_event_rule" "guardduty_forward" {
  name = "aws-ir-forward-guardduty"
  event_pattern = jsonencode({
    source        = ["aws.guardduty"]
    "detail-type" = ["GuardDuty Finding"]
  })
}

resource "aws_cloudwatch_event_target" "security_bus" {
  rule     = aws_cloudwatch_event_rule.guardduty_forward.name
  arn      = var.security_event_bus_arn
  role_arn = aws_iam_role.event_forwarder.arn
}
