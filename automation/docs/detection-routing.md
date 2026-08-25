# Detection-to-response routing

Phase 3 Commit 5 adds a deliberately conservative routing layer between AWS detections and response automation.

## Safety posture

1. Event patterns are source-specific rather than catch-all.
2. The normalizer validates the EventBridge account field and can enforce an explicit account allowlist.
3. Raw finding payloads are not forwarded into Step Functions. The normalized record retains only the minimum routing fields plus a SHA-256 digest of the original event.
4. DynamoDB conditional writes suppress duplicate findings for a configurable TTL window.
5. CloudTrail events from configured automation principal prefixes can be suppressed to reduce response loops.
6. The default route is `notify_only`.
7. Automatic `triage` is read-only, EC2-only, and always uses `dry_run: true`.
8. No EventBridge rule in this release starts live containment.

## Routing matrix

| Signal | Minimum pattern | EC2 extraction | Default route | Optional low-risk automation |
|---|---|---:|---|---|
| GuardDuty | medium+ finding | Yes, when `instanceDetails.instanceId` exists | Notify | Read-only triage |
| Security Hub CSPM | medium/high/critical imported finding | Yes, for `AwsEc2Instance` resources | Notify | Read-only triage |
| AWS Config | `NON_COMPLIANT` | Yes for EC2 resource IDs | Notify | Read-only triage |
| CloudWatch | alarm enters `ALARM` | Not assumed | Notify | None |
| CloudTrail | selected trail-tampering APIs | No | Notify | None |

## Incomplete context

A detection is not proof of compromise. When a finding lacks an EC2 target, contains an unsupported resource type, or cannot be mapped safely, the router falls back to notify-only behavior. Responders should enrich the incident using CloudTrail, GuardDuty/Security Hub details, Config history, and the relevant runbook before containment.

## False positives

Use source-native suppression first when appropriate (for example, GuardDuty suppression rules or Security Hub workflow processes). The repository-level deduplication table is only a delivery-control mechanism; it is not a finding lifecycle system.

## Loop prevention

`IGNORE_PRINCIPAL_ARN_PREFIXES` is intended for project automation roles that could appear in CloudTrail events. Keep the list narrow. Do not suppress whole AWS services or broad account namespaces.
