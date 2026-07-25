# `notify_incident` — Publish an incident notification

## Purpose

Publish a structured incident update to the configured SNS topic after dry-run review.

## Invocation contract

- **Required fields:** `incident_id`, `severity`, `message`; `topic_arn` may be supplied or read from `INCIDENT_TOPIC_ARN`.
- **Mutation:** Yes. Publishing occurs only when `dry_run` is exactly `false`.
- **Sample event:** [`notify-incident-dry-run.json`](../../samples/notify-incident-dry-run.json)
- **IAM example:** [`notify-incident-policy.json`](../../iam/policies/notify-incident-policy.json)
- **Handler:** `app.handler`

See the common [event contract](../../docs/event-contract.md), [safety model](../../docs/safety-model.md), and [rollback manifest specification](../../docs/rollback-manifests.md).

## Result behavior

`planned` or `completed`.

Every result contains `action`, `incident_id`, `dry_run`, `status`, and `details`. Mutating actions return the planned or completed resource changes in `details`; containment actions that support automated restoration also return a `rollback_manifest`.

## Safety and validation

1. The topic ARN must be in the selected Region and current caller account.
2. Do not include credentials, secrets, or large forensic artifacts in the message.
3. SNS is a notification channel, not a durable incident case system.

## Rollback

SNS delivery cannot generally be recalled. Correct an inaccurate notification with a follow-up incident update.

## Operational verification

1. Invoke the sample with identifiers from an authorized lab account.
2. Review the structured output before any non-dry-run request.
3. Confirm the matching CloudTrail event and Lambda request ID.
4. Verify the target resource state independently with the AWS CLI or console.
5. Attach the result and any rollback manifest to the incident record.

## Related runbooks

- [CloudWatch detection and alerting](../../../docs/18-cloudwatch-detection-alerting.md)
