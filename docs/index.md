# Documentation Index

This index organizes the repository by responder task. During an active incident, begin with triage and evidence preservation, then select the closest scenario or domain.

## Immediate response

1. [Classify severity](incident-severity-matrix.md).
2. [Perform initial triage](initial-triage-checklist.md).
3. [Begin evidence collection](evidence-collection-checklist.md).
4. Use the [decision guide](decision-trees.md) when containment or recovery choices are unclear.
5. Select a [domain index](domains/README.md) or scenario runbook.
6. Record actions in the [incident record](../templates/incident-record.md) and [evidence log](../templates/evidence-log.csv).

## Browse by domain

- [Compute and workload response](domains/compute-workloads.md)
- [Identity and account response](domains/identity-account.md)
- [Data, storage, and database response](domains/data-storage-databases.md)
- [Detection, audit, and compliance](domains/detection-audit-compliance.md)
- [Network, automation, and recovery](domains/network-automation-recovery.md)

## Scenario runbooks

| # | Scenario | Domain |
|---:|---|---|
| 1 | [EC2 instance compromise](01-ec2-instance-compromise.md) | Compute |
| 2 | [Automated EC2 isolation](02-automated-ec2-isolation.md) | Automation |
| 3 | [IAM credential compromise](03-iam-credential-compromise.md) | Identity |
| 4 | [Data exfiltration](04-data-exfiltration.md) | Data protection |
| 5 | [Public S3 bucket](05-public-s3-bucket.md) | Storage |
| 6 | [Compliance enforcement](06-compliance-enforcement.md) | Compliance |
| 7 | [RDS database security](07-rds-database-security.md) | Database |
| 8 | [Backdoor IAM user](08-backdoor-iam-user.md) | Identity |
| 9 | [Malicious Lambda or scheduled persistence](09-malicious-lambda-scheduled-persistence.md) | Serverless |
| 10 | [Root account compromise](10-root-account-compromise.md) | Account |
| 11 | [Auto Scaling recovery](11-auto-scaling-recovery.md) | Recovery |
| 12 | [Unauthorized API calls](12-unauthorized-api-calls.md) | Investigation |
| 13 | [Athena CloudTrail investigation](13-athena-cloudtrail-investigation.md) | Investigation |
| 14 | [Systems Manager investigation](14-systems-manager-investigation.md) | Compute |
| 15 | [AWS Config drift](15-aws-config-drift.md) | Compliance |
| 16 | [Security group open to the world](16-security-group-open-to-world.md) | Network |
| 17 | [CloudTrail audit and tampering](17-cloudtrail-audit-tampering.md) | Audit |
| 18 | [CloudWatch detection and alerting](18-cloudwatch-detection-alerting.md) | Detection |
| 19 | [EBS snapshot and forensic preservation](19-ebs-snapshot-forensic-preservation.md) | Forensics |
| 20 | [Step Functions incident orchestration](20-step-functions-incident-orchestration.md) | Orchestration |

## Decision support and governance

- [Incident-response decision guide](decision-trees.md)
- [AWS service mapping](service-mapping.md)
- [Framework mapping](framework-mapping.md)
- [Authoritative reference catalog](references.md)
- [Incident severity matrix](incident-severity-matrix.md)
- [Initial triage checklist](initial-triage-checklist.md)
- [Evidence collection checklist](evidence-collection-checklist.md)

## Emergency procedures

- [IAM emergency lockdown](iam-emergency-lockdown.md)
- [Ransomware response](ransomware-response.md)
- [S3 data-leak response](s3-data-leak-response.md)

## Cheat sheets, queries, templates, and diagrams

- [Service cheat sheets](../cheat-sheets/)
- [AWS CLI incident-response reference](../cheat-sheets/aws-cli-incident-response.md)
- [CloudTrail Athena query library](../queries/cloudtrail-athena.sql)
- [Incident record template](../templates/incident-record.md)
- [Evidence log template](../templates/evidence-log.csv)
- [Diagram source catalog](../diagrams/README.md)

## Project documentation

- [Main README](../README.md)
- [Roadmap](../ROADMAP.md)
- [Changelog](../CHANGELOG.md)
- [Release history](../releases/README.md)
- [Contributing guide](../CONTRIBUTING.md)
- [Security policy](../SECURITY.md)
- [Code of Conduct](../CODE_OF_CONDUCT.md)
