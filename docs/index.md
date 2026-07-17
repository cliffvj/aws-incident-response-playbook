# Documentation Index

This index organizes the repository by responder task rather than file location. During an active incident, begin with triage and evidence preservation before selecting a scenario-specific runbook.

## Immediate response

1. [Classify severity](incident-severity-matrix.md).
2. [Perform initial triage](initial-triage-checklist.md).
3. [Begin evidence collection](evidence-collection-checklist.md).
4. Select the closest scenario runbook below.
5. Record actions in the [incident record template](../templates/incident-record.md) and [evidence log](../templates/evidence-log.csv).

## Scenario runbooks

### Compute, workload, and recovery

- [01 — EC2 instance compromise](01-ec2-instance-compromise.md)
- [02 — Automated EC2 isolation](02-automated-ec2-isolation.md)
- [11 — Auto Scaling recovery](11-auto-scaling-recovery.md)
- [14 — Systems Manager investigation](14-systems-manager-investigation.md)
- [19 — EBS snapshot and forensic preservation](19-ebs-snapshot-forensic-preservation.md)

### Identity and account compromise

- [03 — IAM credential compromise](03-iam-credential-compromise.md)
- [08 — Backdoor IAM user](08-backdoor-iam-user.md)
- [10 — Root account compromise](10-root-account-compromise.md)
- [12 — Unauthorized API calls](12-unauthorized-api-calls.md)
- [IAM emergency lockdown](iam-emergency-lockdown.md)

### Data, storage, and databases

- [04 — Data exfiltration](04-data-exfiltration.md)
- [05 — Public S3 bucket](05-public-s3-bucket.md)
- [07 — RDS database security](07-rds-database-security.md)
- [S3 data-leak response](s3-data-leak-response.md)
- [Ransomware response](ransomware-response.md)

### Detection, audit, and compliance

- [06 — Compliance enforcement](06-compliance-enforcement.md)
- [13 — Athena CloudTrail investigation](13-athena-cloudtrail-investigation.md)
- [15 — AWS Config drift](15-aws-config-drift.md)
- [17 — CloudTrail audit and tampering](17-cloudtrail-audit-tampering.md)
- [18 — CloudWatch detection and alerting](18-cloudwatch-detection-alerting.md)

### Network and automation

- [09 — Malicious Lambda or scheduled persistence](09-malicious-lambda-scheduled-persistence.md)
- [16 — Security group open to the world](16-security-group-open-to-world.md)
- [20 — Step Functions incident orchestration](20-step-functions-incident-orchestration.md)

## Decision support

- [AWS service mapping](service-mapping.md)
- [Incident-response decision trees](decision-trees.md)
- [Incident severity matrix](incident-severity-matrix.md)
- [Initial triage checklist](initial-triage-checklist.md)
- [Evidence collection checklist](evidence-collection-checklist.md)

## Cheat sheets

- [AWS CLI incident-response reference](../cheat-sheets/aws-cli-incident-response.md)
- [Amazon Athena](../cheat-sheets/athena.md)
- [AWS CloudTrail](../cheat-sheets/cloudtrail.md)
- [Amazon CloudWatch](../cheat-sheets/cloudwatch.md)
- [AWS Config](../cheat-sheets/config.md)
- [AWS Identity and Access Management](../cheat-sheets/iam.md)
- [AWS Systems Manager](../cheat-sheets/systems-manager.md)

## Queries, templates, and scripts

- [CloudTrail Athena query library](../queries/cloudtrail-athena.sql)
- [Incident record template](../templates/incident-record.md)
- [Evidence log template](../templates/evidence-log.csv)
- [AWS context verification script](../scripts/verify-context.sh)

## Project documentation

- [Roadmap](../ROADMAP.md)
- [Changelog](../CHANGELOG.md)
- [Contributing guide](../CONTRIBUTING.md)
- [Security policy](../SECURITY.md)
- [Code of Conduct](../CODE_OF_CONDUCT.md)
- [Main README](../README.md)



## Decision intelligence

- [Incident-response decision guide](decision-trees.md) — cross-scenario triage, evidence, containment, identity, automation, recovery, and closure gates.
- [Incident severity matrix](incident-severity-matrix.md) — default severity and escalation criteria.
- [Initial triage checklist](initial-triage-checklist.md) — first-response actions and evidence requirements.

## Framework alignment

- [Framework mapping guide](framework-mapping.md) — MITRE ATT&CK, NIST CSF 2.0 / SP 800-61r3, and AWS Well-Architected cross-reference.

## Visual documentation

- [Diagram source catalog](../diagrams/README.md)
- [Incident-response lifecycle](../diagrams/incident-response-lifecycle.mmd)
- [Automated containment reference](../diagrams/automated-containment-reference.mmd)
- [CloudTrail and Athena investigation](../diagrams/cloudtrail-athena-investigation.mmd)
- [Trusted recovery boundary](../diagrams/recovery-trust-boundary.mmd)

Each numbered runbook now includes an incident snapshot and a GitHub-rendered Mermaid response flow.
