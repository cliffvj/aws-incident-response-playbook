# Event Contract

Every action accepts one JSON object. All actions require a stable incident identifier. Mutating actions default to dry-run when `dry_run` is omitted.

```json
{
  "incident_id": "INC-2026-0001",
  "expected_account_id": "111122223333",
  "region": "us-east-1",
  "dry_run": true,
  "requested_by": "analyst@example.invalid",
  "reason": "Concise incident-response rationale"
}
```

## Common fields

| Field | Required | Description |
|---|---:|---|
| `incident_id` | Yes | Stable case or ticket identifier using letters, numbers, `.`, `_`, `:`, `/`, or `-`. |
| `expected_account_id` | Recommended | Twelve-digit account ID compared with the Lambda caller account before target access. |
| `region` | Required for regional targets | Explicit AWS Region. Lambda environment Region is used only when omitted. |
| `dry_run` | Required operationally for writes | Must be the JSON boolean `false` to perform a write; strings such as `"false"` are rejected. |
| `requested_by` | Recommended | Human or system requesting the action. |
| `reason` | Recommended | Concise, non-sensitive response rationale. |
| `rollback_manifest` | Restore actions | Exact manifest returned by the corresponding containment action. |
| `confirm_restore` | Restore actions | Must be the JSON boolean `true`, including during dry-run restoration review. |

## Resource fields

| Domain | Fields |
|---|---|
| EC2 instance | `instance_id` |
| EC2 isolation | `instance_id`, `quarantine_security_group_id` |
| Quarantine group | `vpc_id` |
| IAM access key | `user_name`, `access_key_id` |
| S3 bucket | `bucket_name`, `region` |
| SNS notification | `severity`, `message`, optional `topic_arn` |

Identifiers are validated before AWS API calls. Cross-account operation is not supported in this commit; use the Lambda execution role in the target account and set `expected_account_id`.

## Common result

```json
{
  "action": "contain_s3_public_access",
  "incident_id": "INC-2026-0003",
  "dry_run": true,
  "status": "planned",
  "details": {}
}
```

Supported status values are action-dependent:

- `observed` — read-only collection completed.
- `planned` — a change is required but was not executed.
- `completed` — a synchronous change completed.
- `submitted` — an asynchronous AWS operation was accepted.
- `no_change` — the requested state already existed.

Unknown event fields are ignored by the current functions. Never place credentials, secrets, raw object data, memory dumps, large forensic artifacts, or sensitive customer content in invocation events or rollback manifests.
