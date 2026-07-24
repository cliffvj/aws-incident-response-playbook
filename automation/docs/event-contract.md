# Event Contract

Every action accepts a JSON object. Mutating actions require:

```json
{
  "incident_id": "INC-2026-0001",
  "dry_run": true,
  "requested_by": "analyst@example.invalid"
}
```

## Common fields

| Field | Required | Description |
|---|---:|---|
| `incident_id` | Yes | Stable case or ticket identifier. |
| `dry_run` | Yes for writes | Must be exactly `false` to perform a write. |
| `requested_by` | Recommended | Human or system requesting the action. |
| `reason` | Recommended | Concise response rationale. |
| `region` | Optional | Explicit AWS Region; otherwise Lambda environment Region is used. |

Unknown fields are preserved in the input but ignored by the current functions. Never place credentials, secrets, full forensic artifacts, or sensitive customer data in invocation events.
