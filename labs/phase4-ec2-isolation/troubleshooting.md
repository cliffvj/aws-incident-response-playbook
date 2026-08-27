# Troubleshooting

## Target never becomes Online in Systems Manager

Check:

```bash
aws ec2 describe-instances --instance-ids "$LAB_INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].[State.Name,IamInstanceProfile.Arn,PublicIpAddress]' \
  --output table

aws ssm describe-instance-information \
  --filters "Key=InstanceIds,Values=$LAB_INSTANCE_ID" \
  --output json
```

Common causes are the wrong Region, missing instance-profile permissions, SSM Agent startup delay, or unavailable outbound HTTPS/DNS connectivity.

Amazon Linux 2023 commonly includes SSM Agent, but the lab still verifies management status rather than assuming it.

## `simulate_suspicious_activity.py` returns `InvalidInstanceId`

The instance might not yet be registered/Online in Systems Manager, or your CLI/boto3 session might be pointed at a different Region or account.

## EventBridge reports a failed entry

Confirm the boto3 session Region and inspect the returned `ErrorCode`/`ErrorMessage`. The lab sends only one custom event, so `FailedEntryCount` should be zero.

## No incident notification arrives

Check the lab EventBridge rule target, Lambda permission, normalizer CloudWatch Logs, duplicate-suppression table, and the Phase 3 `detection_default_route`. Reusing the same finding ID intentionally produces the same dedupe key and can be suppressed as a duplicate.

Generate a new scenario with a new finding ID when repeating detection tests:

```bash
python3 labs/phase4-ec2-isolation/scripts/prepare_scenario.py \
  --instance-id "$LAB_INSTANCE_ID" \
  --account-id "$AWS_ACCOUNT_ID" \
  --region "$AWS_REGION" \
  --requested-by "YOUR_RESPONDER_ID" \
  --finding-id "phase4-ec2-isolation-002"
```

## SSM evidence fails to upload

Confirm the instance role has the exact `ssm_evidence_node_policy_arn` produced by the Phase 3 platform and that the target is in the same Region as the SSM evidence resources used for the exercise.

## Isolation succeeds but Systems Manager disconnects

That can be expected. The quarantine security group is deliberately ruleless. The lab collects host evidence before isolation for this reason.

## `verify_isolation.py` says the ENI is not isolated

Wait for the Step Functions execution to reach `SUCCEEDED`, then inspect the ENIs directly:

```bash
aws ec2 describe-network-interfaces \
  --filters "Name=attachment.instance-id,Values=$LAB_INSTANCE_ID" \
  --query 'NetworkInterfaces[].{ENI:NetworkInterfaceId,Groups:Groups[].{Id:GroupId,Name:GroupName}}' \
  --output table
```

Do not manually force a security-group change merely to satisfy the validator. Investigate the workflow output first.

## Terraform provider binary appears in `git status` or push is rejected for a large file

Never commit `.terraform/`. Remove the local cache from the Git index/history before pushing and confirm the repository root `.gitignore` is present.

```bash
git ls-files | grep -E '(^|/)\.terraform(/|$)'
```

The command should return no tracked Terraform cache paths.
