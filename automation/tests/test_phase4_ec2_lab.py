from pathlib import Path
import importlib.util
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "labs" / "phase4-ec2-isolation"
SCRIPT = LAB / "scripts" / "prepare_scenario.py"

spec = importlib.util.spec_from_file_location("phase4_prepare_scenario", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class Phase4Ec2IsolationLabTests(unittest.TestCase):
    def test_incident_id_is_deterministic(self):
        kwargs = dict(
            instance_id="i-0123456789abcdef0",
            account_id="111122223333",
            region="us-east-1",
            requested_by="unit-test",
            finding_id="phase4-ec2-isolation-simulated-001",
        )
        first = module.build_inputs(**kwargs)
        second = module.build_inputs(**kwargs)
        self.assertEqual(first["incident_id"], second["incident_id"])
        self.assertTrue(first["incident_id"].startswith("EVT-"))

    def test_live_containment_is_explicit_and_scoped(self):
        values = module.build_inputs(
            instance_id="i-0123456789abcdef0",
            account_id="111122223333",
            region="us-east-1",
            requested_by="unit-test",
            finding_id="phase4-ec2-isolation-simulated-001",
        )
        containment = values["containment"]
        self.assertEqual(containment["mode"], "containment")
        self.assertFalse(containment["dry_run"])
        self.assertEqual(containment["expected_account_id"], "111122223333")
        self.assertEqual(containment["instance_id"], "i-0123456789abcdef0")

    def test_terraform_safety_invariants(self):
        text = (LAB / "terraform" / "main.tf").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"\bingress\s*\{", text))
        self.assertIsNone(re.search(r"from_port\s*=\s*22\b", text))
        self.assertRegex(text, r'http_tokens\s*=\s*"required"')
        self.assertRegex(text, r"encrypted\s*=\s*true")
        self.assertRegex(text, r'source\s*=\s*\["aws-ir\.lab"\]')
        self.assertIn('"Simulated Security Finding"', text)

    def test_sample_event_is_explicit_simulation(self):
        sample = json.loads((LAB / "events" / "sample-simulated-finding.json").read_text(encoding="utf-8"))
        self.assertEqual(sample["source"], "aws-ir.lab")
        self.assertEqual(sample["detail-type"], "Simulated Security Finding")
        self.assertTrue(sample["detail"]["simulation"])
        self.assertEqual(sample["detail"]["scenario"], "phase4-ec2-isolation")


if __name__ == "__main__":
    unittest.main()
