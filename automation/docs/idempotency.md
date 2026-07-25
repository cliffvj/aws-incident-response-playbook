# Idempotency and Repeat Invocation

Incident automation must tolerate retries without blindly repeating destructive or billable changes.

## Current controls

| Action | Repeat-invocation behavior |
|---|---|
| EC2 isolation | Compares each network interface with the quarantine group and changes only non-matching interfaces. |
| EC2 restoration | Compares each interface with manifest state and restores only differences. |
| Quarantine group | Reuses a same-name, same-VPC group only when it has no ingress or egress rules. |
| EBS snapshots | Searches for a non-error snapshot tagged with the same incident ID, source volume ID, and manager tag. |
| IAM key disable/restore | Reads current key status and returns `no_change` when it already matches the target. |
| S3 contain/restore | Compares the current bucket-level Block Public Access state with the target state. |
| SNS notification | No automatic deduplication; the operator controls repeated publication. |

## Operator rule

Do not interpret a Lambda timeout as proof that the AWS API failed. Before retrying:

1. Review the Lambda request log.
2. Review CloudTrail for the target API call.
3. Read the target resource's current state.
4. Reinvoke in dry-run mode.
5. Continue only when the returned plan is understood.

## Scope limits

This commit does not include a durable idempotency table, distributed lock, event deduplication key, or orchestration execution token. Those controls are planned for Step Functions and event-driven integration. Current idempotency is state-based and action-local.
