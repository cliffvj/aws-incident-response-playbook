# AWS Organizations deployment pattern

These examples demonstrate a **hub-and-spoke event-forwarding pattern**, not centralized cross-account containment. Member accounts forward selected security events to a security-account event bus protected by an `aws:PrincipalOrgID` condition. Response actions should continue to execute in the target account unless an organization has explicitly designed and reviewed cross-account response roles.

This distinction preserves the current same-account validation in the Lambda response actions.
