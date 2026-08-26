# Terraform state management and upgrade

`v2.6.0` moves the former root resources into reusable modules. `moved.tf` maps the known `v2.5.0` resource addresses to their new nested module addresses.

## Existing deployments

1. Back up the current state.
2. Update code without applying.
3. Run `terraform init -upgrade`.
4. Run `terraform plan`.
5. Expect **address moves**, not broad replacement. Investigate any unexpected destroy/create action before apply.
6. Only after the plan is understood should an authorized operator apply it.

For remote state, copy `backend.tf.example` to `backend.tf`, replace placeholders, and use a dedicated versioned state bucket. Modern S3 backends can use the lockfile mechanism. Keep state access restricted because state can contain infrastructure identifiers and configuration values.

## Import and drift

If a resource exists but is missing from state, use `terraform import` against the **new module address**. Avoid importing production resources merely to silence a plan; first determine why state drift occurred.
