# Upgrade, rollback, and teardown

## Upgrade

- Pin repository releases or Git tags in automation workflows.
- Review release notes and Terraform plans between versions.
- Preserve state backups before structural refactors.
- Keep `moved.tf` until all active states have crossed the v2.6.0 migration.

## Rollback

A code rollback is not always an infrastructure rollback. If Terraform already changed live resources, inspect current state and plan before checking out an older tag. Never restore old state files blindly.

## Teardown

For isolated lab accounts, use `terraform plan -destroy` before `terraform destroy`. Evidence buckets, snapshots, event archives, and KMS keys have retention or deletion semantics that may intentionally outlive compute. Follow the evidence-retention policy before deleting incident artifacts.
