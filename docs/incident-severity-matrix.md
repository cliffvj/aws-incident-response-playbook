# Incident Severity Matrix

| Severity | Criteria | Target response | Examples |
|---|---|---|---|
| SEV-1 Critical | Active material compromise, root takeover, destructive activity, or confirmed sensitive-data exfiltration | Immediate executive/security leadership engagement and continuous response | Root compromise; ransomware spreading; ongoing regulated-data theft |
| SEV-2 High | Confirmed compromise with contained or limited impact | Urgent coordinated response | Compromised admin key; public sensitive S3 bucket with access evidence |
| SEV-3 Medium | Suspicious activity or significant control failure without confirmed compromise | Same-business-day triage | Public SSH; disabled detailed monitoring; anomalous API calls |
| SEV-4 Low | Minor deviation, informational finding, or improvement item | Normal queue | Missing noncritical tag; tuning recommendation |

Severity must be adjusted for data sensitivity, business criticality, scope, duration, regulatory obligations, and confidence.
