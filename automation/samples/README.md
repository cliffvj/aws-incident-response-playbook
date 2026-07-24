# Sample Events

All supplied mutation examples use `"dry_run": true`. Replace placeholder IDs only in an authorized lab account. Validate events locally before invoking Lambda.

```bash
aws lambda invoke --function-name <name> --payload fileb://automation/samples/isolate-ec2-dry-run.json response.json
```
