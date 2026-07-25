# Tests

The test suite uses `unittest` and mocked AWS clients. It does not call AWS.

```bash
python3 -m pip install -r automation/requirements-dev.txt
python3 -m unittest discover -s automation/tests -p 'test_*.py'
python3 automation/scripts/validate_json.py
python3 automation/scripts/check_action_contracts.py
python3 automation/scripts/package_lambdas.py
```

Coverage includes:

- identifier, dry-run, and confirmation validation
- account and Region-aware action behavior
- rollback manifest checksum and resource validation
- EC2 multi-interface isolation and restoration planning
- quarantine security-group create/reuse behavior
- EBS snapshot duplicate prevention
- IAM key ownership, disablement, and restoration planning
- S3 inspection, containment, idempotency, and restoration
- package contents and action-catalog completeness

These are unit and contract tests, not substitutes for authorized AWS integration tests.
