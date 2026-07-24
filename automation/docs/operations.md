# Operating Procedure

1. Confirm identity with `aws sts get-caller-identity`.
2. Confirm Region and target resource ownership.
3. Create or reference the incident record.
4. Invoke with `dry_run: true`.
5. Review the planned action and original-state fields.
6. Preserve required evidence.
7. Obtain approval.
8. Invoke with `dry_run: false`.
9. Verify CloudTrail and target resource state.
10. Record result, timestamps, request ID, and rollback information.

Do not retry a mutating action blindly. First determine whether the prior invocation succeeded, partially succeeded, or timed out after the AWS API accepted the request.
