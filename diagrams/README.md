# Diagram Sources

This directory stores Mermaid source files used by the AWS Incident Response Playbook. GitHub renders Mermaid directly inside Markdown, while the standalone `.mmd` files make diagrams reusable in presentations, documentation sites, and future export pipelines.

## Conventions

- Use `flowchart TD` for procedural runbooks and `flowchart LR` for lifecycle or architecture views.
- Keep node text concise and operational.
- Do not place account IDs, customer names, real incident identifiers, credentials, or sensitive resource names in diagrams.
- Treat automation paths as examples requiring authorization, validation, error handling, and rollback controls.

## Overview diagrams

- `incident-response-lifecycle.mmd`
- `automated-containment-reference.mmd`
- `cloudtrail-athena-investigation.mmd`
- `recovery-trust-boundary.mmd`

## Scenario diagrams

The files prefixed `01-` through `20-` correspond directly to the numbered scenario runbooks in `docs/`.
