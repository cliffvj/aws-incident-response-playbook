# Tests

```bash
python3 -m pip install -r automation/requirements-dev.txt
python3 -m unittest discover -s automation/tests -p 'test_*.py'
python3 automation/scripts/validate_json.py
python3 automation/scripts/package_lambdas.py
```

Tests mock `boto3.client`; they do not call AWS.
