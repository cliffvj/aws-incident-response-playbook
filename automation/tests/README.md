# Automation Tests

Run from the repository root inside an optional virtual environment:

```bash
python3 -m pip install -r automation/requirements-dev.txt
python3 -m compileall -q automation
python3 -m unittest discover -s automation/tests -p 'test_*.py'
python3 automation/scripts/validate_json.py
python3 automation/scripts/check_action_contracts.py
python3 automation/scripts/validate_state_machines.py
python3 automation/scripts/package_lambdas.py
```

Commit 3 adds structural tests for the Step Functions definition. They verify transition targets, callback task-token states, duplicate-event locking, and the separation of live containment/rollback from approval decisions.

These tests do not replace an authorized AWS integration exercise. Terraform validation and a dry-run state-machine execution should pass before any live approval path is attempted.

## Systems Manager document validation

Phase 3 Commit 4 adds `test_ssm_documents.py` and `automation/scripts/validate_ssm_documents.py`. They enforce:

- Automation schema version `0.3`;
- required incident, instance, evidence, and assume-role parameters;
- Online + platform preflight logic;
- Run Command S3 output configuration;
- SHA-256 evidence-manifest finalization; and
- absence of a small denylist of obviously mutating host commands.

These are structural safety checks, not a substitute for an authorized AWS lab execution.
