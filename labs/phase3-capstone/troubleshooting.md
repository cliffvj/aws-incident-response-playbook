# Phase 3 Capstone Troubleshooting

## Instance never becomes SSM Online

Check the EC2 state, public IP, instance profile, and SSM registration. Confirm the instance profile has `AmazonSSMManagedInstanceCore`, outbound HTTPS is available, and the AWS Region is consistent.

## Simulated event accepted but no notification appears

Inspect the lab EventBridge rule and `/aws/lambda/<normalizer-name>` CloudWatch Logs. Reusing the same `finding_id` and target can be suppressed by DynamoDB deduplication; generate a new finding ID for an intentional replay.

## SSM evidence collection fails preflight

The Automation fails closed when the target is unmanaged, offline, or on the wrong platform. Collect evidence **before** network isolation.

## Containment waits indefinitely

The workflow is probably waiting for a callback task token. Confirm the approval SNS path and inspect the execution state. Do not reuse the same `event_id` for a new execution.

## Instance becomes unreachable after approval

Expected: the quarantine security group is ruleless, so Systems Manager can go offline after containment. Use the pre-containment SSM evidence and AWS control-plane telemetry.

## Rollback helper cannot find a manifest

Confirm the containment execution reached successful isolation. If containment failed before isolation, there may be no network state to restore.

## Terraform destroy reports dependency errors

Rollback the target before destroy so the original lab security group is attached. Response-created snapshots and quarantine groups are outside the target-lab Terraform state and require an explicit retention/cleanup decision.
