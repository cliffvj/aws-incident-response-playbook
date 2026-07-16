# AWS Incident Response Service Mapping

Use the question in the third column before selecting a service. A service is not a response phase by itself; responders normally combine identity, evidence, containment, remediation, and validation controls.

| Need | Primary services | Decision question |
|---|---|---|
| Investigation and API timeline | AWS CloudTrail; Amazon Athena | Who performed which API action, when, from where, and against what resource? |
| Configuration compliance | AWS Config | Is the resource configured according to the required control? |
| Metrics, logs, and alarms | Amazon CloudWatch | What changed operationally, and should an alarm or log pattern trigger response? |
| Notification | Amazon SNS | Who must be informed or what subscriber should receive the event? |
| Single-step automation | AWS Lambda | What narrowly scoped code action should run from a trusted event? |
| Multi-step orchestration | AWS Step Functions | What workflow needs retries, branching, approvals, and execution history? |
| Managed instance response | AWS Systems Manager | How can responders collect data or remediate without opening inbound management ports? |
| Identity containment | AWS IAM | Which user, role, policy, key, or session must be restricted or revoked? |
| Compute containment/recovery | Amazon EC2; EC2 Auto Scaling | How should an instance be isolated, preserved, rebuilt, or replaced? |
| Network containment | Amazon VPC | Which security group, route, subnet, endpoint policy, or NACL limits exposure? |
| Object data exposure | Amazon S3 | Is bucket/object access public, cross-account, logged, encrypted, and recoverable? |
| Database exposure | Amazon RDS | Is the database private, least-privilege, logged, encrypted, and recoverable? |


## Incident lifecycle mapping

| Phase | Typical actions | Common services |
|---|---|---|
| Prepare | Logging, roles, forensic account, automation, exercises | IAM, CloudTrail, Config, S3, Systems Manager, Step Functions |
| Detect | Alarms, configuration changes, suspicious API activity | CloudWatch, Config, CloudTrail, SNS |
| Investigate | Timeline, identity correlation, resource state, log queries | CloudTrail, Athena, S3, CloudWatch, Systems Manager |
| Contain | Revoke credentials, quarantine compute, restrict network/data access | IAM, EC2, VPC, S3, RDS |
| Eradicate | Remove persistence, patch root cause, rotate secrets, rebuild | IAM, Lambda, Systems Manager, EC2 Auto Scaling |
| Recover | Restore trusted service, harden network, validate telemetry | EC2 Auto Scaling, RDS, S3, VPC, CloudWatch, Config |
| Learn | Timeline, control gaps, runbook changes, exercises | CloudTrail, Athena, Config, CloudWatch |

## Microcredential objective map

| Objective | Most likely services |
|---|---|
| Implement audit and compliance controls | CloudTrail, Config, CloudWatch, SNS, Lambda |
| Contain data exfiltration | VPC, EC2, IAM, S3, CloudTrail, Athena |
| Establish database security | RDS, VPC, IAM, CloudWatch, CloudTrail |
| Identify and remediate compromised resources | CloudTrail, Athena, EC2, Systems Manager, Lambda |
| Eradicate backdoor access | IAM, CloudTrail, Lambda, Step Functions |
| Recover with network hardening | VPC, EC2 Auto Scaling, EC2, Config, CloudWatch |

## Authoritative references

- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/welcome.html)
- [AWS Security Incident Response documentation](https://docs.aws.amazon.com/security-ir/)
- [AWS Well-Architected Security Pillar — Incident response](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/incident-response.html)
- [AWS Prescriptive Guidance — Incident response recommendations](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-controls-by-caf-capability/incident-response-recommendations.html)
