# Evidence Collection Checklist

## Metadata
- Incident ID, collector, UTC timestamps, account, Region, resource ARN/ID, source alert.

## Cloud evidence
- CloudTrail events and trail status; Config timeline; CloudWatch logs/metrics/alarms; S3 data/access events; VPC Flow Logs; service-specific logs.
- IAM user/role policies, access-key metadata, role trust policy, session issuer, MFA state.
- Resource configuration JSON before and after containment.
- EBS snapshots, AMI/launch-template details, Lambda package/configuration, RDS snapshots/configuration when applicable.

## Integrity and custody
- Store evidence in a restricted account/bucket, use encryption and retention controls, record hashes where applicable, and analyze copies instead of originals.
