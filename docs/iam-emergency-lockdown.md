# IAM Emergency Lockdown

1. Identify the exact user, role session, access key, federation source, and affected accounts.
2. Preserve credential metadata and CloudTrail evidence.
3. Deactivate exposed long-term keys; revoke active sessions or apply a temporary explicit deny when necessary.
4. Search for privilege escalation and persistence: new identities, keys, policies, trust changes, `PassRole`, logging changes, and cross-account access.
5. Rotate dependent secrets and remove unauthorized objects.
6. Validate legitimate administrator access before broad lockdown to avoid account lockout.
7. Require MFA and short-lived credentials and improve detections.

Never rotate or delete a key without identifying workloads that depend on it and planning a safe replacement.
