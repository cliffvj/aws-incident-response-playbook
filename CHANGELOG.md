# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

## [Unreleased]

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
