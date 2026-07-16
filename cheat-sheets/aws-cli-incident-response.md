# AWS CLI Incident Response Quick Reference

```bash
aws sts get-caller-identity
aws configure list
aws cloudtrail lookup-events --max-results 50
aws ec2 describe-instances --instance-ids i-EXAMPLE
aws ec2 describe-network-interfaces --filters Name=attachment.instance-id,Values=i-EXAMPLE
aws iam get-user --user-name USER
aws iam list-access-keys --user-name USER
aws s3api get-public-access-block --bucket BUCKET
aws rds describe-db-instances --db-instance-identifier DB
aws configservice describe-compliance-by-config-rule
```

Start read-only. Store output securely. Validate account and Region before every write command.
