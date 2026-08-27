# Interview Review — EC2 Compromise and Isolation Lab

Use these prompts after completing the exercise. The goal is to explain decisions, not memorize commands.

## 1. Why collect evidence before isolation?

A strong answer should mention that network isolation can change volatile state and can also sever Systems Manager connectivity. In this lab the responder collects read-only host evidence and preserves EBS storage before changing the instance's security groups.

## 2. Why use Systems Manager instead of SSH?

The target security group intentionally has no inbound administration rules. Systems Manager provides an auditable management plane without opening port 22 and lets the response workflow collect bounded evidence through an approved instance role.

## 3. Why isn't the detection allowed to isolate the instance automatically?

The Phase 3 detection layer normalizes and routes the finding conservatively. High-impact containment still requires explicit responder intent and a Step Functions approval callback. This reduces the risk of a false positive causing an outage.

## 4. Why create EBS snapshots before quarantine?

Snapshots preserve storage state for later analysis and recovery. They are useful storage evidence but are not full forensic images and do not preserve memory or every volatile artifact.

## 5. What makes the rollback safer than simply reattaching a guessed security group?

The containment action records the original network state in a structured rollback manifest with integrity metadata. Restoration validates account, Region, resource, incident, action, and checksum context before applying that recorded state.

## 6. What would you change for production?

Possible discussion points include private subnets/VPC endpoints, organization-specific approval systems, centralized security accounts, stronger evidence-retention controls, production IAM review, alarm/telemetry tuning, change-management integration, and service-owner recovery signoff.

## 30-second project explanation

> I built and exercised an AWS incident-response lab where a benign EC2 finding is routed through EventBridge, investigated through Systems Manager without SSH, preserved with encrypted evidence and EBS snapshots, and then isolated through a Step Functions workflow with human approval. I also validate the quarantine and use a checksummed rollback manifest to restore the original security-group state. The lab is Terraform-deployable and designed for an authorized sandbox rather than production.
