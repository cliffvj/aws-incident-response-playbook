from __future__ import annotations
import json
from pathlib import Path
from unittest import TestCase
ROOT=Path(__file__).resolve().parents[1]
class DetectionPatternTests(TestCase):
    def test_patterns_are_valid_json_and_source_scoped(self):
        for path in (ROOT/"detection"/"event-patterns").glob("*.json"):
            value=json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(value.get("source"), path.name)
            self.assertTrue(value.get("detail-type"), path.name)
    def test_routing_policy_never_enables_live_containment(self):
        value=json.loads((ROOT/"detection"/"routing-policy.json").read_text(encoding="utf-8"))
        self.assertTrue(all(not route["live_containment"] for route in value["routes"]))
