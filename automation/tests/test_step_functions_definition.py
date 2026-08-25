from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


class StepFunctionsDefinitionTests(unittest.TestCase):
    path = Path("automation/step-functions/ec2-incident-response.asl.json")

    def rendered(self) -> dict:
        text = self.path.read_text(encoding="utf-8")
        replacements = {
            "partition": "aws",
            "collect_metadata_arn": "arn:aws:lambda:us-east-1:111122223333:function:collect",
            "snapshot_ebs_arn": "arn:aws:lambda:us-east-1:111122223333:function:snapshot",
            "ensure_quarantine_arn": "arn:aws:lambda:us-east-1:111122223333:function:quarantine",
            "isolate_ec2_arn": "arn:aws:lambda:us-east-1:111122223333:function:isolate",
            "restore_ec2_arn": "arn:aws:lambda:us-east-1:111122223333:function:restore",
            "notify_incident_arn": "arn:aws:lambda:us-east-1:111122223333:function:notify",
            "approval_topic_arn": "arn:aws:sns:us-east-1:111122223333:approval",
            "execution_table_name": "executions",
            "approval_timeout_seconds": "3600",
        }
        text = re.sub(r"\$\{([A-Za-z0-9_]+)\}", lambda m: replacements[m.group(1)], text)
        text = text.replace('"__APPROVAL_TIMEOUT_SECONDS__"', replacements["approval_timeout_seconds"])
        return json.loads(text)

    def test_validator_script(self):
        result = subprocess.run(
            [sys.executable, "automation/scripts/validate_state_machines.py"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_live_actions_require_approval_route(self):
        states = self.rendered()["States"]
        containment = states["EvaluateContainmentApproval"]["Choices"]
        rollback = states["EvaluateRollbackApproval"]["Choices"]
        self.assertEqual(containment[0]["Next"], "EnsureQuarantineLive")
        self.assertEqual(rollback[0]["Next"], "ExecuteRollbackLive")

    def test_duplicate_event_condition(self):
        acquire = self.rendered()["States"]["AcquireExecutionLock"]
        self.assertEqual(acquire["Parameters"]["ConditionExpression"], "attribute_not_exists(event_id)")

    def test_callback_tokens_are_not_sent_to_general_notification_topic(self):
        states = self.rendered()["States"]
        for name in ("RequestContainmentApproval", "RequestRollbackApproval"):
            self.assertIn("waitForTaskToken", states[name]["Resource"])
            self.assertEqual(states[name]["Parameters"]["Message"]["task_token.$"], "$$.Task.Token")
        for name in ("NotifyTriage", "NotifyContainmentPlan", "NotifyContainmentSuccess", "NotifyRollbackPlan", "NotifyRollbackSuccess"):
            self.assertNotIn("$$.Task.Token", json.dumps(states[name]))


if __name__ == "__main__":
    unittest.main()
