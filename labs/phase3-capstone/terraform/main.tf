provider "aws" {
  region = var.aws_region
}

data "aws_partition" "current" {}
data "aws_caller_identity" "current" {}

data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

locals {
  common_tags = merge(
    {
      Project     = "aws-incident-response-playbook"
      Environment = "authorized-lab"
      Phase       = "3-capstone"
      ManagedBy   = "Terraform"
    },
    var.tags,
  )
}

resource "aws_vpc" "lab" {
  cidr_block           = "10.77.0.0/24"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = merge(local.common_tags, { Name = "${var.project_name}-vpc" })
}

resource "aws_internet_gateway" "lab" {
  vpc_id = aws_vpc.lab.id
  tags   = merge(local.common_tags, { Name = "${var.project_name}-igw" })
}

resource "aws_subnet" "target" {
  vpc_id                  = aws_vpc.lab.id
  cidr_block              = "10.77.0.0/26"
  map_public_ip_on_launch = true
  tags                    = merge(local.common_tags, { Name = "${var.project_name}-target" })
}

resource "aws_route_table" "target" {
  vpc_id = aws_vpc.lab.id
  tags   = merge(local.common_tags, { Name = "${var.project_name}-target" })
}

resource "aws_route" "internet" {
  route_table_id         = aws_route_table.target.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.lab.id
}

resource "aws_route_table_association" "target" {
  subnet_id      = aws_subnet.target.id
  route_table_id = aws_route_table.target.id
}

resource "aws_security_group" "target" {
  name        = "${var.project_name}-target"
  description = "No-ingress capstone target; outbound HTTPS only"
  vpc_id      = aws_vpc.lab.id

  egress {
    description = "Outbound HTTPS for Systems Manager and AWS APIs"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, { Name = "${var.project_name}-target" })
}

resource "aws_iam_role" "target" {
  name = "${var.project_name}-ec2"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "ssm_core" {
  role       = aws_iam_role.target.name
  policy_arn = "arn:${data.aws_partition.current.partition}:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_role_policy_attachment" "evidence_write" {
  role       = aws_iam_role.target.name
  policy_arn = var.ssm_evidence_node_policy_arn
}

resource "aws_iam_instance_profile" "target" {
  name = "${var.project_name}-ec2"
  role = aws_iam_role.target.name
}

resource "aws_instance" "target" {
  ami                         = data.aws_ami.al2023.id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.target.id
  vpc_security_group_ids      = [aws_security_group.target.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.target.name

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    encrypted   = true
    volume_type = "gp3"
    volume_size = 8
  }

  user_data = <<-EOT
    #!/bin/bash
    set -eu
    mkdir -p /var/tmp/aws-ir-lab
    cat > /var/tmp/aws-ir-lab/simulated-activity.txt <<'MARKER'
    AUTHORIZED AWS INCIDENT RESPONSE LAB
    This harmless marker represents suspicious activity for an evidence-collection exercise.
    No malware, persistence, exploit, credential theft, or data exfiltration is performed.
    MARKER
    chmod 0644 /var/tmp/aws-ir-lab/simulated-activity.txt
    systemctl enable --now amazon-ssm-agent 2>/dev/null || true
  EOT

  tags = merge(local.common_tags, {
    Name       = "${var.project_name}-target"
    LabPurpose = "benign-suspicious-activity-simulation"
  })

  depends_on = [
    aws_route.internet,
    aws_iam_role_policy_attachment.ssm_core,
    aws_iam_role_policy_attachment.evidence_write,
  ]
}

resource "aws_cloudwatch_event_rule" "simulated_finding" {
  name        = "${var.project_name}-simulated-finding"
  description = "Authorized lab-only simulated AWS IR finding"
  event_pattern = jsonencode({
    source        = ["aws-ir.lab"]
    "detail-type" = ["Simulated Security Finding"]
  })
  tags = local.common_tags
}

resource "aws_cloudwatch_event_target" "normalizer" {
  rule = aws_cloudwatch_event_rule.simulated_finding.name
  arn  = "arn:${data.aws_partition.current.partition}:lambda:${var.aws_region}:${data.aws_caller_identity.current.account_id}:function:${var.detection_normalizer_function_name}"
}

resource "aws_lambda_permission" "eventbridge_lab" {
  statement_id  = "AllowEventBridgePhase3Capstone"
  action        = "lambda:InvokeFunction"
  function_name = var.detection_normalizer_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.simulated_finding.arn
}
