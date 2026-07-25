import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shared"))

from aws_ir.tags import incident_tag_map, incident_tags


class TestTags(unittest.TestCase):
    def test_common_tags(self):
        tags = incident_tag_map("INC-1", "analyst@example.invalid", action="snapshot")
        self.assertEqual(tags["IncidentId"], "INC-1")
        self.assertEqual(tags["ManagedBy"], "aws-ir-playbook")
        self.assertEqual(tags["ResponseAction"], "snapshot")

    def test_aws_list_shape(self):
        tags = incident_tags("INC-1", extra={"SourceVolumeId": "vol-123"})
        self.assertIn({"Key": "SourceVolumeId", "Value": "vol-123"}, tags)


if __name__ == "__main__":
    unittest.main()
