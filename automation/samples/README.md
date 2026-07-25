# Sample Events

All supplied mutation examples use `"dry_run": true`. The identifiers, account IDs, ARNs, user names, and bucket names are placeholders. Replace them only for authorized lab resources.

## Collection and preparation

- [`collect-ec2-metadata.json`](collect-ec2-metadata.json)
- [`ensure-quarantine-sg-dry-run.json`](ensure-quarantine-sg-dry-run.json)
- [`inspect-s3-public-access.json`](inspect-s3-public-access.json)

## Containment and evidence

- [`snapshot-ebs-dry-run.json`](snapshot-ebs-dry-run.json)
- [`isolate-ec2-dry-run.json`](isolate-ec2-dry-run.json)
- [`disable-iam-key-dry-run.json`](disable-iam-key-dry-run.json)
- [`contain-s3-public-access-dry-run.json`](contain-s3-public-access-dry-run.json)
- [`notify-incident-dry-run.json`](notify-incident-dry-run.json)

## Restoration

- [`restore-ec2-security-groups-dry-run.json`](restore-ec2-security-groups-dry-run.json)
- [`restore-iam-key-dry-run.json`](restore-iam-key-dry-run.json)
- [`restore-s3-public-access-dry-run.json`](restore-s3-public-access-dry-run.json)

The restoration samples contain valid example checksums. Editing any manifest field without recomputing the checksum causes validation to fail, as intended. In actual incidents, use the exact manifest returned by the containment execution rather than a repository sample.

```bash
python3 automation/scripts/validate_json.py
./automation/scripts/invoke_dry_run.sh \
  aws-ir-lab-contain-s3-public-access \
  automation/samples/contain-s3-public-access-dry-run.json
```
