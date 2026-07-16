# Ransomware Response on AWS

- Isolate affected compute and credentials while preserving logs and snapshots.
- Determine whether encryption is occurring at the guest OS, shared filesystem, S3/API, database, or backup layer.
- Protect clean backups, snapshots, versions, replication destinations, and KMS keys from compromised principals.
- Search CloudTrail for deletion, lifecycle, versioning, snapshot, backup-vault, KMS, and IAM changes.
- Rebuild from trusted images; do not restore malware or compromised bootstrap scripts.
- Validate recovery in an isolated environment before reconnecting production.
- Engage leadership, legal, law enforcement, cyber insurance, and AWS Support according to policy.
