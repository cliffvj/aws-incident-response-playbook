# Scenario 19: EBS Snapshot and Forensic Preservation

> **Objective:** Preserve storage evidence before eradication and maintain a defensible chain of custody.

## Scope and safety

Use this runbook only with authorized access and an assigned incident identifier. Preserve evidence before destructive changes. Commands are examples: verify the account, Region, resource identifiers, dependencies, and rollback path before execution.

## Severity guidance

- **Critical:** confirmed active compromise, root/administrator takeover, or ongoing sensitive-data loss.
- **High:** strong evidence of compromise with material exposure but no confirmed continuing impact.
- **Medium:** suspicious or noncompliant configuration requiring investigation.

## Required evidence

- Incident ID, UTC timeline, responder identity, account and Region
- Relevant CloudTrail events and configuration state
- Resource identifiers, tags, owners, dependencies, and screenshots/exports required by policy
- Every containment/remediation action and its result

## Runbook

1. Record instance and volume metadata, attachment mappings, encryption keys, timestamps, tags, and incident ID.
2. Collect volatile evidence first when required because snapshots do not capture memory or all transient state.
3. Create snapshots of all relevant EBS volumes; consider filesystem/application consistency and document whether the instance was running or stopped.
4. Copy snapshots to a dedicated forensic account/Region where policy requires, re-encrypting with an approved key.
5. Restrict snapshot and KMS access, enable logging, and tag evidence as immutable under organizational process.
6. Analyze copies rather than originals and attach them read-only where tooling permits.
7. Retain or dispose of evidence according to legal, regulatory, and incident-retention requirements.

## AWS CLI starting points

```bash
aws ec2 describe-volumes --filters Name=attachment.instance-id,Values=i-EXAMPLE
aws ec2 create-snapshot --volume-id vol-EXAMPLE --description "IR-CASE-ID forensic snapshot"   --tag-specifications 'ResourceType=snapshot,Tags=[{Key=IncidentId,Value=IR-CASE-ID},{Key=Evidence,Value=true}]'
aws ec2 wait snapshot-completed --snapshot-ids snap-EXAMPLE
```


## Console starting points

- **CloudTrail → Event history** for recent management activity
- **CloudWatch → Logs / Metrics / Alarms** for telemetry
- Relevant service console for current configuration and dependencies
- **Systems Manager** for controlled instance access and automation where supported

## Validation and closure

- The threat is no longer active and unauthorized access has been removed.
- Required evidence is preserved and accessible only to approved responders.
- Business functionality, logging, alarms, backups, and compliance checks pass.
- Root cause, blast radius, timeline, owner, corrective actions, and follow-up dates are recorded.

## Services used

Amazon EC2, Amazon EBS, AWS Identity and Access Management, AWS CloudTrail

## Exam cues

Look for explicit task verbs: **identify**, **enable**, **disable**, **isolate**, **restrict**, **snapshot**, **query**, **notify**, **remediate**, and **validate**. Complete exactly what the lab requests; avoid unrelated improvements that could consume time or break grading dependencies.

## Authoritative references

- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/welcome.html)
- [AWS Security Incident Response documentation](https://docs.aws.amazon.com/security-ir/)
- [AWS Well-Architected Security Pillar — Incident response](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/incident-response.html)
- [AWS Prescriptive Guidance — Incident response recommendations](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-controls-by-caf-capability/incident-response-recommendations.html)

