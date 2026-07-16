# Security Policy

## Purpose

This repository contains defensive AWS incident-response guidance. Documentation and examples can affect real infrastructure, so reports involving unsafe commands, privilege escalation, exposed secrets, or misleading remediation steps are treated seriously.

## Supported versions

Security and safety corrections are applied to the latest version on the default branch. Older tags are retained for release history and may not receive updates.

## Reporting a vulnerability or unsafe instruction

Do **not** open a public issue containing:

- AWS access keys, session tokens, passwords, private keys, or signed URLs.
- AWS account IDs associated with an active incident.
- Customer data, personal data, or regulated information.
- Private investigation artifacts, CloudTrail records, screenshots, or forensic evidence.
- Details that would expose an unpatched weakness in a real environment.

Use GitHub’s private vulnerability reporting feature when it is enabled for the repository. If private reporting is unavailable, contact the repository maintainer through a non-public channel listed on the maintainer’s GitHub profile. Provide only the minimum information needed to reproduce the concern safely.

## What to include

A useful report contains:

- The affected file and section.
- The unsafe, inaccurate, or exploitable behavior.
- Preconditions and likely impact.
- A safe reproduction in an isolated account, when applicable.
- A proposed correction or mitigation, if known.
- Relevant authoritative documentation.

Remove or redact all sensitive identifiers before submission.

## Response expectations

The maintainer will attempt to:

1. Acknowledge a complete report.
2. Assess severity and reproducibility.
3. Correct or remove unsafe guidance.
4. Credit the reporter when requested and appropriate.
5. Document the correction in the changelog when it affects users.

No specific response or remediation time is guaranteed because this is a community-maintained educational project.

## Safe operational use

- Validate every command in an authorized non-production environment.
- Confirm the active AWS identity, account, Region, and resource identifiers.
- Preserve evidence before destructive action whenever feasible.
- Obtain approval for actions that may interrupt services or alter evidence.
- Do not assume examples implement complete least privilege for every environment.
- Engage your incident commander, legal counsel, compliance team, and AWS Support as required by organizational policy.

## Scope limitations

This repository is not a managed incident-response service, a guarantee of regulatory compliance, or a substitute for organization-specific procedures. AWS services, APIs, and console workflows change over time; always compare guidance with current AWS documentation before production use.
