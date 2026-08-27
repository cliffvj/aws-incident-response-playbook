# Authorized AWS Incident Response Labs

This directory contains deliberately scoped, authorized practice environments for validating repository runbooks and automation without using production resources.

## Phase 4 practice labs

| Lab | Release | Purpose |
|---|---|---|
| [EC2 compromise investigation and isolation](phase4-ec2-isolation/README.md) | `v3.1.0` | Deploy a benign EC2 target, simulate a finding, collect SSM evidence, preserve EBS state, quarantine the instance through approved orchestration, verify containment, and restore the original network state. |

The Phase 4 labs are scenario-specific exercises. They reuse the Phase 3 response platform where that improves realism and keeps response controls consistent.

## Phase 3 capstone

[phase3-capstone/](phase3-capstone/README.md) validates the Phase 3 response platform end to end with a benign EC2 target, a simulated EventBridge security finding, read-only Systems Manager evidence collection, human-approved Step Functions containment, verification, and rollback.

The labs do **not** deploy malware, exploit vulnerabilities, steal credentials, create malicious persistence, exfiltrate data, or perform destructive testing unless a future exercise explicitly documents a safe alternative and authorization boundary.

## Rules

- Use a dedicated AWS lab account or clearly isolated sandbox.
- Verify account and Region before every deployment and response action.
- Review `terraform plan` before every apply.
- Keep high-impact response mutation behind documented human approval.
- Collect evidence before containment when the scenario permits it.
- Treat callback task tokens, credentials, account identifiers, and evidence as sensitive.
- Destroy lab resources after validation and separately review retained evidence/snapshots.
- Never commit `.terraform/`, Terraform state, generated lab inputs, evidence, or Python cache files.
