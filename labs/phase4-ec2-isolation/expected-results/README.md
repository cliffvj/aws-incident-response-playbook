# Expected Results Checklist

Use this checklist while performing the lab. Record actual IDs and timestamps in your own incident notes rather than editing this file with live account identifiers.

## Deployment

- [ ] Terraform creates one VPC, subnet, internet gateway, route table, no-ingress target security group, IAM instance role/profile, EC2 target, EventBridge rule/target, and Lambda invoke permission.
- [ ] EC2 root EBS volume is encrypted.
- [ ] EC2 metadata options require IMDSv2.
- [ ] Target security group has zero ingress rules.
- [ ] Target is `Online` in Systems Manager.

## Simulation and detection

- [ ] SSM Run Command creates `/var/tmp/aws-ir-practice/simulated-suspicious-activity.txt`.
- [ ] `prepare_scenario.py` emits an `EVT-...` deterministic incident ID.
- [ ] EventBridge accepts the custom event with zero failed entries.
- [ ] The detection normalizer accepts the `aws-ir.lab` event.
- [ ] Recommended `notify_only` routing does not start live containment automatically.

## Investigation

- [ ] Linux SSM evidence Automation completes successfully.
- [ ] Evidence is written under an incident/instance/execution-specific S3 prefix.
- [ ] `integrity-manifest.json` is present.
- [ ] Manifest verification succeeds.
- [ ] Recent `/var/tmp` metadata contains evidence of the benign marker.

## Containment

- [ ] Step Functions execution correlates to the deterministic incident ID.
- [ ] EBS snapshot action completes before network isolation approval.
- [ ] Workflow pauses for human approval.
- [ ] After approval, all target ENIs use only `aws-ir-quarantine-<incident-id>`.
- [ ] No automatic rollback occurs simply because containment succeeded.

## Recovery

- [ ] Rollback input is extracted from the successful execution output.
- [ ] Rollback manifest checksum is validated by the response action.
- [ ] Restoration requires its own approval.
- [ ] Original security-group associations are restored.
- [ ] SSM returns `Online` after connectivity is restored and sufficient time has elapsed.

## Teardown

- [ ] Terraform target-lab destroy completes.
- [ ] Evidence snapshots are reviewed separately.
- [ ] S3 evidence retention is reviewed separately.
- [ ] No `.terraform/`, state, generated input, callback token, or account-specific evidence is committed to Git.
