# Scenario 12: Unauthorized API Calls

> **Objective:** Investigate suspicious AWS API activity and contain the responsible principal.

## Scope and safety

Use this runbook only with authorized access and an assigned incident identifier. Preserve evidence before destructive changes. Commands are examples: verify the account, Region, resource identifiers, dependencies, and rollback path before execution.


## Incident snapshot

| Item | Value |
|---|---|
| Default severity | **High** — adjust using the [severity matrix](incident-severity-matrix.md) |
| Primary impact | AWS control plane |
| Response objective | Attribute activity and contain principal |
| AWS services | AWS CloudTrail, Amazon Athena, AWS IAM, Amazon CloudWatch |
| Automation role | Optional |
| Typical execution window | 20–60 minutes; actual duration depends on scope and approvals |

> [!NOTE]
> Severity and timing are planning defaults, not substitutes for business-impact assessment, legal guidance, or the incident commander’s decision.

## Response flow

```mermaid
flowchart TD
    A["Suspicious API event"]
    B["Identify principal and source"]
    C["Build UTC timeline"]
    D["Determine affected resources"]
    E["Restrict principal or session"]
    F["Reverse unauthorized changes"]
    G["Validate logging and alerts"]
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
```

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

1. Capture eventName, eventSource, eventTime, awsRegion, sourceIPAddress, userAgent, requestParameters, resources, and userIdentity.
2. Correlate by access key ID, principal ARN, role session name, session issuer, source IP, user agent, and adjacent timestamps.
3. Determine whether the event was successful and identify all resources created, changed, accessed, or deleted.
4. Contain the principal through credential deactivation, session revocation, or temporary deny controls.
5. Check for anti-forensics and persistence, especially logging changes, policy changes, new identities, new keys, and cross-account trust.
6. Remediate affected resources and rotate dependent credentials.
7. Create a timeline and validate no suspicious activity remains in other Regions or accounts.

## AWS CLI starting points

```bash
# Start with read-only discovery. Substitute verified identifiers and Region.
aws sts get-caller-identity
aws cloudtrail lookup-events --max-results 50
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

AWS CloudTrail, Amazon Athena, AWS Identity and Access Management, Amazon SNS

## Exam cues

Look for explicit task verbs: **identify**, **enable**, **disable**, **isolate**, **restrict**, **snapshot**, **query**, **notify**, **remediate**, and **validate**. Complete exactly what the lab requests; avoid unrelated improvements that could consume time or break grading dependencies.

## Authoritative references

- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/welcome.html)
- [AWS Security Incident Response documentation](https://docs.aws.amazon.com/security-ir/)
- [AWS Well-Architected Security Pillar — Incident response](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/incident-response.html)
- [AWS Prescriptive Guidance — Incident response recommendations](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-controls-by-caf-capability/incident-response-recommendations.html)


---

[Documentation index](index.md) · [Previous scenario](11-auto-scaling-recovery.md) · [Next scenario](13-athena-cloudtrail-investigation.md)
