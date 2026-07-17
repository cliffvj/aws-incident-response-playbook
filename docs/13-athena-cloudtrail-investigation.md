# Scenario 13: Athena CloudTrail Investigation

> **Objective:** Use Athena to search centralized CloudTrail logs at scale.

## Scope and safety

Use this runbook only with authorized access and an assigned incident identifier. Preserve evidence before destructive changes. Commands are examples: verify the account, Region, resource identifiers, dependencies, and rollback path before execution.


## Incident snapshot

| Item | Value |
|---|---|
| Default severity | **Medium** — adjust using the [severity matrix](incident-severity-matrix.md) |
| Primary impact | Centralized audit logs |
| Response objective | Search CloudTrail efficiently |
| AWS services | Amazon Athena, Amazon S3, AWS Glue Data Catalog, AWS CloudTrail |
| Automation role | Manual |
| Typical execution window | 20–45 minutes; actual duration depends on scope and approvals |

> [!NOTE]
> Severity and timing are planning defaults, not substitutes for business-impact assessment, legal guidance, or the incident commander’s decision.

## Response flow

```mermaid
flowchart TD
    A["Investigation question"]
    B["Define time, account, and Region"]
    C["Select partitioned log data"]
    D["Run scoped Athena query"]
    E["Validate event context"]
    F["Export evidence securely"]
    G["Document findings"]
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

1. Confirm CloudTrail logs are delivered to the correct S3 prefix and determine account, Region, and date partitions.
2. Create an Athena table using CloudTrail table creation or partition projection and use a dedicated encrypted query-results location.
3. Limit queries by event date, account, Region, event source, event name, and principal to reduce cost and noise.
4. Parse nested userIdentity, requestParameters, responseElements, and resources fields carefully; handle JSON strings where needed.
5. Export investigation results with an incident ID and preserve query text, execution ID, and result location.
6. Correlate suspicious activity across identity, network, storage, compute, and logging events.
7. Drop temporary tables or revoke access after the investigation while retaining required evidence under policy.

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

Amazon Athena, AWS CloudTrail, Amazon S3

## Exam cues

Look for explicit task verbs: **identify**, **enable**, **disable**, **isolate**, **restrict**, **snapshot**, **query**, **notify**, **remediate**, and **validate**. Complete exactly what the lab requests; avoid unrelated improvements that could consume time or break grading dependencies.

## Authoritative references

- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/welcome.html)
- [AWS Security Incident Response documentation](https://docs.aws.amazon.com/security-ir/)
- [AWS Well-Architected Security Pillar — Incident response](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/incident-response.html)
- [AWS Prescriptive Guidance — Incident response recommendations](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-controls-by-caf-capability/incident-response-recommendations.html)


---

[Documentation index](index.md) · [Previous scenario](12-unauthorized-api-calls.md) · [Next scenario](14-systems-manager-investigation.md)
