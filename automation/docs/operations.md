# Operating Procedure

## Before invocation

1. Confirm identity with `aws sts get-caller-identity`.
2. Confirm account, Region, target resource ownership, and incident ID.
3. Open or reference the incident record.
4. Review the action README and least-privilege execution policy.
5. Confirm evidence preservation requirements and the approved sequence of actions.
6. Validate the rollback path or document why automated rollback is intentionally unavailable.

## Dry-run review

1. Invoke with `dry_run: true`.
2. Confirm the result's account, Region, resource identifiers, current state, and proposed changes.
3. Save any rollback manifest with the incident record.
4. Confirm the action returns `planned`, `no_change`, or `observed` as expected.
5. Obtain change approval for non-dry-run execution.

## Execution

1. Invoke the same reviewed event with `dry_run: false`.
2. Record Lambda request ID and timestamp.
3. Verify CloudTrail and the target resource independently.
4. Record partial completion, asynchronous state, and any manual follow-up.
5. Publish an incident update without including secrets or raw evidence.

## Restoration

1. Retrieve the exact manifest from the approved containment execution.
2. Confirm the incident, resource, account, Region, and recovery decision.
3. Set `confirm_restore: true` and keep `dry_run: true`.
4. Review the restoration plan and current target state.
5. Obtain separate restoration approval.
6. Set `dry_run: false`, invoke, verify, and document.

Do not retry a mutating action blindly. First determine whether the prior invocation succeeded, partially succeeded, or timed out after AWS accepted the API request.\n## Step Functions operations\n\nUse `event_id` as the one-time execution request identifier and `incident_id` as the broader case identifier. During review, correlate Step Functions execution ARN, DynamoDB status, Lambda request logs, CloudTrail, evidence snapshots, approval identity, and returned rollback manifests.\n\nNever retry a failed execution by blindly reusing the same `event_id`; inspect the current resource state first and then create a new event ID if a rerun is justified.\n

## Systems Manager investigation operations

Use `automation/scripts/start_ssm_investigation.sh` for a controlled lab execution. Record the returned Automation execution ID in the incident record. A successful collection is not complete until `FinalizeIntegrityManifest` succeeds and the responder can retrieve `integrity-manifest.json`.

Recommended operator sequence:

1. verify AWS account, Region, instance ID, incident ID, and change/evidence authorization;
2. verify the target is `Online` in Systems Manager;
3. start the platform-specific Automation document;
4. watch `get-automation-execution` for failed or timed-out steps;
5. retrieve the manifest and run `verify_evidence_manifest.py`;
6. link the S3 prefix, Automation execution ID, Run Command ID, and manifest hash to the incident record;
7. perform containment only through a separately approved workflow.
