# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Phase 4 deployable practice labs.

## [3.0.0] — 2026-08-25

### Added

- Authorized Phase 3 end-to-end EC2 incident-response capstone lab.
- Standalone target-lab Terraform for a benign Amazon Linux target with no inbound security-group rules, encrypted root volume, IMDSv2 enforcement, SSM instance profile, and lab-only EventBridge integration.
- Deterministic simulated-finding and live-containment input generator.
- Lab-only `aws-ir.lab` EventBridge finding injection helper.
- Read-only SSM evidence step before network isolation.
- Isolation verifier and completed-execution rollback-input extractor using the checksummed Lambda rollback manifest.
- Capstone safety validator, unit tests, troubleshooting, cost/retention boundaries, teardown instructions, and portfolio checklist.

### Changed

- Phase 3 status is complete at the `v3.0.0` automated response platform milestone.
- CI validates both platform and capstone Terraform roots.

### Safety

- The capstone uses a harmless marker rather than malware, exploit code, credential theft, persistence, or exfiltration.
- Detection does not auto-start live containment; containment and rollback retain human callback approval.
- Host evidence is collected before ruleless network isolation.

### Validation

- Capstone checks require no inbound target SG rules, IMDSv2, encrypted root storage, lab-only EventBridge scoping, and generated-input exclusion from Git.

## [2.6.0] — 2026-08-25

### Added

- Reusable Terraform modules for notification, logging, IAM, response actions, orchestration, SSM investigation, event routing, and the composed platform.
- Lab, development, and controlled-production adaptation examples.
- AWS Organizations security-account/member-account event-forwarding pattern that deliberately stops short of implicit cross-account containment.
- Optional IAM permissions-boundary support and configurable KMS deletion windows.
- S3 backend example, state migration guidance, `moved` blocks for known v2.5.0 resource addresses, import/upgrade/rollback/teardown documentation.
- Security-oriented Terraform static checks in CI.

### Changed

- The root Terraform deployment now composes `modules/platform` instead of defining the full stack directly.
- Terraform outputs remain compatible at the root while implementation resources move under modules.

### Safety

- Cross-account event aggregation is documented separately from cross-account response authority.
- Controlled-production examples are explicitly adaptation templates, not production approval.
- Existing same-account validation in response actions remains intact.

### Validation

- Python, JSON, action, Step Functions, SSM, event-pattern, Markdown, and Terraform security-oriented static validation remain in CI.
- `terraform fmt`, `terraform init -backend=false`, `terraform validate`, and a reviewed `terraform plan` are required before apply.

## [2.5.0] — 2026-08-25

### Added

- EventBridge patterns for medium-or-higher GuardDuty findings, Security Hub CSPM imported findings, AWS Config noncompliance, CloudWatch ALARM transitions, and selected CloudTrail tampering APIs.
- Detection normalizer Lambda that minimizes raw finding propagation, maps severity/resource context, and preserves a SHA-256 source-event digest.
- DynamoDB TTL-based duplicate suppression, source-account allowlisting, and principal-prefix loop suppression.
- Conservative notify-only routing plus optional read-only EC2 triage through the existing Step Functions workflow.
- EventBridge retry policies, encrypted SQS dead-letter queue, optional event archive, and replay/operator guidance.
- Optional CloudWatch Logs `AccessDenied` metric filter/alarm bridge, disabled unless a log group is provided.
- Event-pattern samples, structural validation, normalizer unit tests, IAM reference policy, Terraform resources, and operator test helper.

### Safety

- Live containment is never started automatically by the detection layer in this release.
- `detection_default_route` defaults to `notify_only`; automatic `triage` is EC2-only and always uses `dry_run: true`.
- Unsupported or incomplete resource context falls back to notification rather than guessed remediation.
- Duplicate suppression and loop controls reduce repeated or self-generated response triggers.

### Validation

- Event patterns and samples are checked as JSON and source/detail-type scoped.
- Unit tests cover GuardDuty, Security Hub, CloudTrail, duplicate handling, notify-only routing, and dry-run triage.
- Terraform formatting and validation remain enforced by GitHub Actions and documented for local execution.

## [2.4.0] — 2026-08-25

### Added

- Read-only Linux and Windows Systems Manager Automation documents for EC2 host investigation without opening SSH or RDP.
- Managed-node preflight that fails closed when the instance is unmanaged, not `Online`, or on the wrong platform.
- Linux collection for process, network, service, package, user/logon, scheduled-task, kernel/mount, recent temporary-file metadata, and bounded selected logs.
- Windows collection for process, network, service, hotfix/software, local-user/session, scheduled-task, and bounded System/Application/Security event metadata.
- Versioned S3 evidence bucket with Block Public Access, TLS-only bucket policy, SSE-KMS default encryption, KMS key rotation, S3 Bucket Keys, and configurable lifecycle retention.
- Post-collection SHA-256 integrity manifest covering every Run Command output object, collection metadata, Automation execution ID, and Run Command ID.
- Local evidence-manifest verifier, SSM execution helper, structural SSM-document validator, samples, collection-scope documentation, and Mermaid evidence-flow diagram.
- Dedicated Automation role, supplemental managed-node evidence-write policy, and responder start/read policy; the latter two are not attached automatically.
- Terraform resources and outputs for evidence storage, KMS, IAM, and the Linux/Windows Automation documents.

### Changed

- Automation documentation now treats Systems Manager as a separate host-evidence plane, independent from Step Functions containment/remediation.
- Scenario 14 now links directly to the deployable Phase 3 investigation implementation.
- GitHub Actions automation validation now checks SSM Automation document safety/structure.

### Safety

- Host collection is read-only by design and does not stop services, patch, delete files, quarantine the instance, or change network controls.
- Linux/Windows collection aborts before Run Command when SSM management status, connectivity, or platform checks fail.
- Evidence is partitioned by incident ID, instance ID, Automation execution ID, and platform.
- Sensitive host output is protected with access-controlled SSE-KMS storage; evidence-write and responder-read policies are not broadly attached.
- Linux is the primary lab-validation target; Windows requires the same account-specific testing before broader use; macOS remains unsupported.

### Validation

- JSON validation covers both SSM Automation documents and samples.
- SSM structural validation enforces preflight, Run Command S3 output, integrity-manifest finalization, and a denylist of obvious mutating commands.
- Unit tests cover document platform selection, preflight checks, read-only collection shape, and SHA-256 finalization.
- Terraform formatting and validation remain enforced by GitHub Actions and documented for local execution.

## [2.3.0] — 2026-08-25

### Added

- Reference AWS Step Functions Standard Workflow for EC2 triage, evidence preservation, approved containment, and approved rollback.
- Dedicated KMS-encrypted approval SNS topic using the callback task-token pattern.
- DynamoDB execution-correlation table with conditional `event_id` duplicate suppression.
- Structured terminal outcomes for planned, successful, denied, timed-out, invalid-approval, duplicate, failed, and partial-failure paths.
- Bounded Lambda retries, catches, approval timeouts, and explicit partial-failure handling without blind automatic compensation.
- Terraform resources for the state machine, execution role, approval topic, correlation table, Step Functions logs, and a standalone human-approver callback policy.
- Step Functions architecture and execution-path Mermaid sources, dry-run triage/containment/rollback samples, approval-response samples, and operator helper scripts.
- ASL structural validator and unit tests that enforce approval boundaries and duplicate-event controls.
- Runbook, documentation index, IAM, operations, safety, troubleshooting, cost, and Terraform cross-references for orchestration.

### Changed

- Phase 3 automation now includes an orchestration layer while retaining independent Lambda action boundaries.
- Live EC2 containment preserves EBS evidence before requesting approval for network isolation.
- Live rollback validates and dry-runs the restoration plan before requesting human approval.
- Step Functions execution-data logging defaults to disabled because callback task tokens and incident context may be sensitive.

### Safety

- Missing orchestration `dry_run` defaults to `true`.
- Live network containment and live rollback cannot proceed through the reference workflow without a successful callback decision of `APPROVE`.
- Approval task tokens use a dedicated SNS topic and are not sent through the general incident-notification action.
- Duplicate `event_id` values stop before response actions execute.
- Partial containment failures do not automatically erase evidence or undo isolation.

### Validation

- ASL template rendering and transition validation are enforced locally and in GitHub Actions.
- Unit tests verify callback-token separation, approval routing, and duplicate-event locking.
- Terraform formatting and validation remain enforced by GitHub Actions.

## [2.2.0] — 2026-07-25

### Added

- Six additional Lambda actions for quarantine security-group preparation, EC2 security-group restoration, S3 public-access inspection, S3 public-access containment, S3 Block Public Access restoration, and IAM access-key restoration.
- Checksummed rollback manifests with incident, resource, account, Region, action, state, and integrity validation.
- State-based idempotency for EC2 isolation and restoration, EBS snapshots, IAM key status changes, S3 containment and restoration, and quarantine security-group reuse.
- S3 inspection of bucket-level Block Public Access, bucket policy, policy status, ACL, and Object Ownership before containment.
- Machine-readable action catalog and automated action-contract validation.
- Expanded IAM policies, Terraform deployment scopes, dry-run events, rollback event examples, operator guidance, troubleshooting, cost, cleanup, and action-level documentation.
- Thirty-one mocked unit tests covering validation, manifests, tags, EC2, IAM, S3, snapshot, packaging, and action contracts.
- Complete project roadmap covering Phases 1 through 6, target releases, dependencies, engineering standards, risk controls, success measures, and definitions of done.
- Versioned release notes and complete Phase 3 Commit 2 installation instructions.

### Changed

- EC2 isolation now evaluates and changes every attached network interface rather than relying only on the instance's primary security-group attribute.
- EBS snapshot creation now tags source instance and volume IDs and avoids duplicate incident/source-volume snapshots.
- IAM key disablement now verifies the key belongs to the supplied user and returns a rollback manifest with the original status.
- SNS notification now validates that the topic belongs to the selected account and Region.
- Terraform now deploys all eleven response actions with one role and log group per function and explicit S3 bucket and IAM user scope variables.
- Expanded `ROADMAP.md` into the authoritative project planning and governance document and marked Commit 2 complete.
- Updated runbooks and repository navigation with direct automation and rollback references.

### Safety

- Mutating actions continue to default to `dry_run: true`.
- Restore actions require `confirm_restore: true` and a valid matching rollback manifest.
- S3 containment changes only bucket-level Block Public Access and preserves bucket policy and ACL documents unchanged.
- Cross-account and cross-Region mismatches fail closed.
- Quarantine security groups must have no ingress or egress rules before use.

### Validation

- Python compilation, JSON validation, action-contract validation, Lambda packaging, and 31 unit tests pass locally.
- Terraform formatting and validation are enforced by GitHub Actions and documented for local execution.

## [2.1.0] — 2026-07-24

### Added

- Dry-run-first response automation framework under `automation/`.
- Five modular Python Lambda actions for EC2 metadata collection, EC2 isolation, EBS snapshot creation, IAM access-key disablement, and SNS notification.
- Shared event validation, structured logging, AWS context, tagging, and response helpers.
- Least-privilege IAM policy examples and an explicit permissions matrix.
- Terraform deployment scaffold for Lambda functions, IAM roles, CloudWatch log groups, and an encrypted SNS topic.
- Sample invocation events, local packaging scripts, unit tests, and GitHub Actions automation validation.
- Versioned release notes and complete Phase 3 Commit 1 installation instructions.

### Changed

- Marked Phase 3 as in progress in the main README and roadmap.
- Expanded repository navigation to include automation and deployment resources.

### Safety

- Mutating actions default to `dry_run: true` and require explicit identifiers.
- EC2 isolation records original security-group associations in the response for rollback planning.
- Automation is intentionally not connected to automatic detection triggers in this commit.

## [2.0.0] — 2026-07-17

### Added

- Domain-oriented documentation indexes for compute, identity, data, detection, and automation/recovery response.
- Central authoritative-reference catalog covering AWS, NIST, and MITRE sources.
- Release-history index under `releases/README.md`.
- Repository-local Markdown link validator and GitHub Actions documentation validation workflow.
- Phase 2 completion and Phase 3 handoff documentation.

### Changed

- Completed cross-navigation among scenario runbooks, decision support, framework mappings, domain indexes, and source references.
- Updated the main README, documentation index, roadmap, and pull-request template for the production-documentation milestone.
- Marked Phase 2 as complete and identified response automation as the next project phase.

### Validation

- Reviewed internal Markdown links and relative paths.
- Consolidated authoritative references to reduce duplication and simplify maintenance.
- Preserved the operational content of all twenty runbooks.

## [1.4.0] — 2026-07-17

### Added

- Decision checkpoints tailored to all 20 incident-response runbooks.
- Central decision guide for severity, evidence preservation, containment selection, identity response, trusted recovery, automation approval, and closure.
- Mermaid decision paths for incident entry, evidence-before-action, identity containment, and recovery trust validation.
- Versioned release notes for v1.4.0.

### Changed

- Expanded README and documentation-index navigation for decision support.
- Added cross-scenario decision-support links to every runbook.

## [1.3.0] — 2026-07-17

### Added

- Framework alignment sections in all 20 scenario runbooks.
- Central MITRE ATT&CK, NIST CSF 2.0 / SP 800-61r3, and AWS Well-Architected mapping guide.
- Repository-wide pull request template with validation and safety checks.
- Versioned release notes for v1.3.0.

### Changed

- Expanded README and documentation-index navigation for framework mappings.
- Clarified that ATT&CK mappings represent plausible technique context and require evidence confirmation.

## [1.2.0] — 2026-07-17

### Added

- Incident snapshot tables for all 20 scenario runbooks.
- GitHub-rendered Mermaid response flows for every scenario.
- Reusable Mermaid source files under `diagrams/`.
- Visual-documentation catalog and architecture-level diagrams.
- Previous, next, and index navigation links in each scenario runbook.

### Changed

- Improved README navigation and lab-safety guidance.
- Expanded the documentation index with visual resources.

## [1.1.0] — 2026-07-17

### Added

- Task-oriented documentation index at `docs/index.md`.
- Project roadmap with phased milestones.
- Community Code of Conduct.
- Structured changelog and release policy.

### Changed

- Redesigned the main README with badges, quick navigation, categorized runbooks, project status, and safer operational guidance.
- Expanded the contribution guide with workflow, content standards, validation requirements, and commit conventions.
- Expanded the security policy with disclosure guidance and handling rules for sensitive incident information.

## [1.0.0] — 2026-07-16

### Added

- Twenty AWS incident-response scenario runbooks.
- Service mapping and incident-response decision trees.
- Severity, initial triage, and evidence-collection guidance.
- IAM emergency lockdown, ransomware, and S3 data-leak procedures.
- AWS service cheat sheets.
- AWS CLI incident-response command reference.
- Athena CloudTrail investigation query library.
- Incident record and evidence-log templates.
- AWS context-verification helper script.
- MIT License, contribution guidance, and security policy.
