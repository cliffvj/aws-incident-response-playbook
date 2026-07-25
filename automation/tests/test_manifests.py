import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "shared"))

from aws_ir.errors import ValidationError
from aws_ir.manifests import create_manifest, validate_manifest


class TestManifests(unittest.TestCase):
    def setUp(self):
        self.manifest = create_manifest(
            action="contain_s3_public_access",
            incident_id="INC-1",
            resource_type="s3-bucket",
            resource_id="bucket-1",
            account_id="111122223333",
            region="us-east-1",
            state={"public_access_block": {"present": False, "configuration": None}},
        )

    def test_valid_manifest(self):
        validated = validate_manifest(
            self.manifest,
            expected_action="contain_s3_public_access",
            expected_resource_type="s3-bucket",
            expected_resource_id="bucket-1",
            expected_incident_id="INC-1",
        )
        self.assertEqual(validated["manifest_version"], 1)

    def test_tampering_is_detected(self):
        changed = copy.deepcopy(self.manifest)
        changed["state"]["public_access_block"]["present"] = True
        with self.assertRaises(ValidationError):
            validate_manifest(
                changed,
                expected_action="contain_s3_public_access",
                expected_resource_type="s3-bucket",
            )

    def test_wrong_resource_is_rejected(self):
        with self.assertRaises(ValidationError):
            validate_manifest(
                self.manifest,
                expected_action="contain_s3_public_access",
                expected_resource_type="s3-bucket",
                expected_resource_id="another-bucket",
            )


if __name__ == "__main__":
    unittest.main()
