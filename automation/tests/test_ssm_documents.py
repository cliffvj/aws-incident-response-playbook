from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


class SsmDocumentTests(unittest.TestCase):
    linux_path = Path("automation/ssm/collect-linux-evidence.json")
    windows_path = Path("automation/ssm/collect-windows-evidence.json")

    def load(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_validator_script(self):
        result = subprocess.run(
            [sys.executable, "automation/scripts/validate_ssm_documents.py"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_linux_is_read_only_run_command_collection(self):
        document = self.load(self.linux_path)
        steps = {value["name"]: value for value in document["mainSteps"]}
        collect = steps["CollectLinuxEvidence"]
        self.assertEqual(collect["action"], "aws:runCommand")
        self.assertEqual(collect["inputs"]["DocumentName"], "AWS-RunShellScript")
        self.assertIn("OutputS3BucketName", collect["inputs"])

    def test_windows_is_read_only_run_command_collection(self):
        document = self.load(self.windows_path)
        steps = {value["name"]: value for value in document["mainSteps"]}
        collect = steps["CollectWindowsEvidence"]
        self.assertEqual(collect["inputs"]["DocumentName"], "AWS-RunPowerShellScript")
        self.assertNotIn("Win32_Product", json.dumps(collect))

    def test_preflight_requires_online_correct_platform(self):
        for path, expected in ((self.linux_path, "Linux"), (self.windows_path, "Windows")):
            document = self.load(path)
            preflight = document["mainSteps"][0]
            script = preflight["inputs"]["Script"]
            self.assertIn('ping_status != "Online"', script)
            self.assertIn("platform_type != expected_platform", script)
            self.assertEqual(preflight["inputs"]["InputPayload"]["expected_platform"], expected)

    def test_integrity_manifest_hashes_s3_objects(self):
        for path in (self.linux_path, self.windows_path):
            document = self.load(path)
            finalizer = document["mainSteps"][2]
            script = finalizer["inputs"]["Script"]
            self.assertIn("hashlib.sha256", script)
            self.assertIn("s3.get_object", script)
            self.assertIn("integrity-manifest.json", script)


if __name__ == "__main__":
    unittest.main()
