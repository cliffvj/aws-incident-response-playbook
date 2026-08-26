# Authorized AWS Incident Response Labs

This directory contains deliberately scoped, authorized practice environments for validating repository automation without using production resources.

## Phase 3 capstone

[phase3-capstone/](phase3-capstone/README.md) validates the Phase 3 response platform end to end with a benign EC2 target, a simulated EventBridge security finding, read-only Systems Manager evidence collection, human-approved Step Functions containment, verification, and rollback.

The lab does **not** deploy malware, exploit a vulnerability, create persistence, exfiltrate data, or perform destructive testing. The suspicious condition is a harmless marker file created during instance bootstrap.

## Rules

- Use a dedicated AWS lab account or clearly isolated sandbox.
- Review `terraform plan` before every apply.
- Keep response mutation behind the documented human approval gate.
- Collect evidence before containment when the scenario permits it.
- Destroy lab resources after validation and verify that the Phase 3 platform is destroyed separately when no longer required.
