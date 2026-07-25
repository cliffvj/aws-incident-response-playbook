# Response Actions

This guide groups the Lambda actions into operator workflows. Detailed input fields, IAM policies, verification, and rollback steps are in each action's README.

## EC2 containment sequence

1. [`collect_ec2_metadata`](../lambda/collect_ec2_metadata/README.md)
2. [`snapshot_ebs_volumes`](../lambda/snapshot_ebs_volumes/README.md)
3. [`ensure_quarantine_security_group`](../lambda/ensure_quarantine_security_group/README.md)
4. [`isolate_ec2_instance`](../lambda/isolate_ec2_instance/README.md)
5. [`notify_incident`](../lambda/notify_incident/README.md)
6. [`restore_ec2_security_groups`](../lambda/restore_ec2_security_groups/README.md) only after trusted recovery approval

## IAM access-key sequence

1. Confirm the key/user relationship and last-used data through [`disable_iam_access_key`](../lambda/disable_iam_access_key/README.md) dry-run.
2. Investigate CloudTrail use, adjacent credentials, policies, sessions, and persistence.
3. Disable the key after authorization.
4. Prefer replacement and deletion. Use [`restore_iam_access_key`](../lambda/restore_iam_access_key/README.md) only when the captured credential must be re-enabled for a justified recovery path.

## S3 public-access sequence

1. Capture policy, ACL, Object Ownership, policy status, and Block Public Access with [`inspect_s3_public_access`](../lambda/inspect_s3_public_access/README.md).
2. Determine whether public access is intended and whether active exposure requires immediate containment.
3. Run [`contain_s3_public_access`](../lambda/contain_s3_public_access/README.md) in dry-run mode and preserve the manifest.
4. Enable all four bucket-level controls after approval.
5. Verify application impact, access paths, policy status, CloudTrail data events when configured, and exposure scope.
6. Use [`restore_s3_public_access`](../lambda/restore_s3_public_access/README.md) only after a reviewed recovery decision.

## Phase boundary

The actions remain independent in Commit 2. Step Functions sequencing, retry/catch behavior, approval states, and compensation paths are introduced in Commit 3.
