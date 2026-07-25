# Rollback Manifests

Containment actions that support automated restoration return a rollback manifest under `details.rollback_manifest`.

## Format

```json
{
  "manifest_version": 1,
  "action": "isolate_ec2_instance",
  "incident_id": "INC-2026-0001",
  "captured_at": "2026-07-24T00:00:00+00:00",
  "resource": {
    "type": "ec2-instance",
    "id": "i-0123456789abcdef0",
    "account_id": "111122223333",
    "region": "us-east-1"
  },
  "state": {},
  "metadata": {},
  "checksum_sha256": "..."
}
```

The checksum is calculated over the canonical JSON form of every manifest field except the checksum itself. It detects accidental edits and simple tampering but is **not** a digital signature and does not prove who created or authorized the manifest.

## Validation performed by restore actions

- supported manifest version
- expected source action
- expected resource type and ID
- matching incident ID
- matching caller account and Region
- checksum consistency
- action-specific state structure
- explicit `confirm_restore: true`

## Storage procedure

1. Save the complete dry-run result before authorizing containment.
2. Save the complete non-dry-run result after containment.
3. Store manifests in the incident case system or encrypted evidence location with access logging and retention controls.
4. Do not copy only the `state` field; restoration requires the full manifest.
5. Record who approved containment and who approved restoration separately.
6. Re-run restoration in dry-run mode and independently inspect the plan before setting `dry_run` to `false`.

## Supported rollback pairs

| Containment action | Restore action | Captured state |
|---|---|---|
| `isolate_ec2_instance` | `restore_ec2_security_groups` | Security-group IDs for every attached network interface |
| `disable_iam_access_key` | `restore_iam_access_key` | IAM user name and original key status |
| `contain_s3_public_access` | `restore_s3_public_access` | Bucket-level Block Public Access presence and configuration, plus policy/ACL context |

## Important limitations

- Deleted network interfaces or security groups cannot be recreated by the EC2 restore action.
- Re-enabling an IAM key can reintroduce a compromised credential; replacement is usually preferable.
- S3 restoration changes only bucket-level Block Public Access because containment deliberately leaves policy and ACL documents unchanged.
- Restoring prior state does not prove that prior state is secure or appropriate after the incident.
