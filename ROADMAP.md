# Project Roadmap

This roadmap describes the planned evolution of the AWS Incident Response Playbook. Priorities may change based on AWS service updates, contributor feedback, and findings from authorized lab validation.

## Phase 1 — Foundation

**Status:** Complete

- [x] Create 20 scenario-based incident-response runbooks.
- [x] Add AWS service mapping.
- [x] Add severity, triage, and evidence-preservation guidance.
- [x] Add emergency IAM, ransomware, and S3 data-leak procedures.
- [x] Add service cheat sheets, CLI references, Athena queries, and templates.
- [x] Add project license, security policy, and contribution guidance.

## Phase 2 — Documentation professionalization

**Status:** Complete

### Commit 1 — Repository polish

- [x] Redesign the main README.
- [x] Add a task-oriented documentation index.
- [x] Add roadmap and changelog files.
- [x] Expand contribution and security guidance.
- [x] Add a community Code of Conduct.

### Commit 2 — Mermaid diagrams

- [x] Add a scenario workflow diagram to every runbook.
- [x] Add architecture diagrams for the major response patterns.
- [x] Add diagram source conventions and accessibility notes.

### Commit 3 — Framework mappings

- [x] Map each scenario to relevant MITRE ATT&CK techniques.
- [x] Map each scenario to the NIST incident-response lifecycle.
- [x] Map each scenario to AWS Well-Architected Security Pillar guidance.
- [x] Clearly separate direct mappings from contextual or inferred mappings.

### Commit 4 — Decision trees

- [x] Add scenario-specific responder decision trees.
- [x] Add escalation and approval checkpoints.
- [x] Add destructive-action safeguards and rollback branches.

### Commit 5 — Navigation and references

- [x] Add consistent previous/next navigation to runbooks.
- [x] Improve cross-references among related scenarios.
- [x] Add authoritative AWS references to each runbook.
- [x] Run a complete Markdown-link and formatting review.

> Phase 2 concluded with release **v2.0.0 — Production Documentation**.

## Phase 3 — Response automation

**Status:** Planned

- [ ] Add a safe EC2 isolation Lambda function.
- [ ] Add IAM access-key disable and session-revocation automation.
- [ ] Add S3 public-access remediation automation.
- [ ] Add Step Functions workflows with approval gates.
- [ ] Add Systems Manager Automation documents.
- [ ] Add CloudFormation and Terraform deployment options.
- [ ] Add automated tests, linting, and least-privilege IAM examples.

## Phase 4 — Deployable practice labs

**Status:** Planned

- [ ] EC2 compromise and quarantine lab.
- [ ] Public S3 exposure lab.
- [ ] Publicly accessible RDS remediation lab.
- [ ] IAM credential compromise investigation lab.
- [ ] CloudTrail and Athena investigation lab.
- [ ] AWS Config compliance-remediation lab.
- [ ] Step Functions orchestration lab.
- [ ] Full incident-response capstone exercise.
- [ ] Cost estimates, teardown steps, and safety controls for every lab.

## Phase 5 — Detection engineering

**Status:** Planned

- [ ] CloudWatch Logs metric-filter library.
- [ ] EventBridge detection patterns.
- [ ] CloudTrail Lake query examples.
- [ ] GuardDuty and Security Hub response patterns.
- [ ] Detection validation and false-positive guidance.

## Phase 6 — Operational maturity

**Status:** Planned

- [ ] Incident commander and responder role cards.
- [ ] Communications and stakeholder-update templates.
- [ ] Tabletop-exercise facilitator guides.
- [ ] Evidence-retention and chain-of-custody procedures.
- [ ] Recovery validation and post-incident review templates.
- [ ] Multi-account and AWS Organizations response patterns.

## Release approach

- Patch releases (`1.1.x`) fix errors, broken links, and minor documentation issues.
- Minor releases (`1.x.0`) add backward-compatible runbooks, diagrams, queries, or automation.
- Major releases (`x.0.0`) introduce significant structural changes or materially revised workflows.

See [CHANGELOG.md](CHANGELOG.md) for completed release history.
