# Contributing

Thank you for helping improve the AWS Incident Response Playbook. Contributions should make response guidance safer, clearer, more accurate, and easier to validate in an authorized AWS environment.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Before contributing

- Search existing issues and pull requests to avoid duplicate work.
- For substantial changes, open an issue describing the proposed scope before implementation.
- Never include real credentials, account IDs, customer data, private IP addressing from a client environment, active incident details, or proprietary evidence.
- Prefer official AWS documentation and primary standards sources.
- Test commands only in an authorized, non-production account unless your organization has approved a controlled production response.

## Contribution types

Useful contributions include:

- Corrections to unsafe, inaccurate, or outdated response steps.
- Additional validation and rollback guidance.
- New investigation queries or read-only responder commands.
- Diagrams, decision trees, framework mappings, or cross-references.
- Improvements to accessibility, clarity, grammar, and navigation.
- Deployable automation with least-privilege IAM and tests.
- Reproducible, low-cost practice labs with complete cleanup steps.

## Content standards

Every runbook or procedure should:

1. State the objective and expected end condition.
2. Separate detection, investigation, containment, eradication, recovery, and validation.
3. Preserve evidence before destructive action whenever feasible.
4. Identify prerequisites, permissions, Regions, and account context.
5. Use placeholders instead of real identifiers.
6. Explain business-impact and rollback considerations.
7. Include a validation method.
8. Cite authoritative sources.
9. Clearly label optional, inferred, or environment-dependent guidance.
10. Avoid implying that one response action is universally correct.

## Command safety

For AWS CLI, SDK, Terraform, CloudFormation, Lambda, and Systems Manager examples:

- Prefer read-only commands during investigation.
- Use explicit placeholder variables such as `${INSTANCE_ID}` and `${AWS_REGION}`.
- Include `aws sts get-caller-identity` or equivalent context verification where appropriate.
- Avoid wildcard IAM permissions unless the example explicitly explains and constrains them.
- Highlight destructive or irreversible commands.
- Provide rollback or recovery guidance for state-changing actions.
- Do not include credential material, signed URLs, session tokens, or copied production output.

## Documentation style

- Use concise headings and complete sentences.
- Define acronyms on first use.
- Use UTC timestamps in incident examples.
- Use fenced code blocks with a language identifier.
- Use relative links for repository content.
- Add alt text or an explanatory caption for diagrams.
- Keep Mermaid node labels short and readable.
- Use GitHub callouts such as `> [!WARNING]` only for meaningful safety information.

## Local workflow

Create a focused branch:

```bash
git checkout -b docs/short-description
```

Review the changes:

```bash
git status
git diff --check
git diff
```

Stage and commit:

```bash
git add <files>
git commit -m "docs: describe the documentation change"
```

Push the branch:

```bash
git push -u origin docs/short-description
```

## Commit messages

Use a clear conventional prefix when practical:

- `docs:` documentation-only changes
- `feat:` new runbooks, automation, queries, or labs
- `fix:` corrections to unsafe or incorrect guidance
- `refactor:` structural changes without a behavioral change
- `test:` validation or automated test additions
- `chore:` repository maintenance

## Pull-request checklist

Before opening a pull request, confirm that:

- [ ] The change is limited to the stated scope.
- [ ] Markdown links resolve correctly.
- [ ] Code blocks and Mermaid diagrams render correctly.
- [ ] Commands use placeholders and include safety context.
- [ ] State-changing actions include validation and rollback guidance.
- [ ] No sensitive information is present.
- [ ] Relevant AWS documentation or primary references are included.
- [ ] The changelog is updated when the change is user-visible.

## Reporting security concerns

Do not report exposed credentials, active incidents, or sensitive account information in a public issue. Follow [SECURITY.md](SECURITY.md) instead.
