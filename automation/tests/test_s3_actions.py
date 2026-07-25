import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from aws_ir.manifests import create_manifest
from aws_ir.s3_state import BLOCK_ALL_PUBLIC_ACCESS
from helpers import client_router, context, load_action, sts

contain = load_action("contain_s3_public_access")
inspect = load_action("inspect_s3_public_access")
restore = load_action("restore_s3_public_access")

BASE_STATE = {
    "public_access_block": {"present": False, "configuration": None},
    "policy": {"present": False, "document": None},
    "policy_status": {"IsPublic": True},
    "acl": {"Owner": {"ID": "owner"}, "Grants": []},
    "ownership_controls": {"Rules": [{"ObjectOwnership": "BucketOwnerEnforced"}]},
}


class TestS3Actions(unittest.TestCase):
    @patch.object(inspect, "capture_bucket_public_access", return_value=BASE_STATE)
    @patch.object(inspect, "bucket_region", return_value="us-east-1")
    @patch.object(inspect.boto3, "client")
    def test_inspect_is_read_only(self, client, _region, _capture):
        client.side_effect = client_router(s3=MagicMock(), sts=sts())
        output = inspect.handler(
            {
                "incident_id": "INC-1",
                "bucket_name": "incident-bucket-123",
                "region": "us-east-1",
            },
            context(),
        )
        self.assertEqual(output["status"], "observed")
        self.assertTrue(output["dry_run"])

    @patch.object(contain, "capture_bucket_public_access", return_value=BASE_STATE)
    @patch.object(contain, "bucket_region", return_value="us-east-1")
    @patch.object(contain.boto3, "client")
    def test_containment_dry_run_returns_manifest(self, client, _region, _capture):
        s3 = MagicMock()
        client.side_effect = client_router(s3=s3, sts=sts())
        output = contain.handler(
            {
                "incident_id": "INC-1",
                "bucket_name": "incident-bucket-123",
                "region": "us-east-1",
                "dry_run": True,
            },
            context(),
        )
        self.assertEqual(output["status"], "planned")
        self.assertIn("rollback_manifest", output["details"])
        s3.put_public_access_block.assert_not_called()

    @patch.object(contain, "capture_bucket_public_access", return_value=BASE_STATE)
    @patch.object(contain, "bucket_region", return_value="us-east-1")
    @patch.object(contain.boto3, "client")
    def test_containment_execute(self, client, _region, _capture):
        s3 = MagicMock()
        client.side_effect = client_router(s3=s3, sts=sts())
        output = contain.handler(
            {
                "incident_id": "INC-1",
                "bucket_name": "incident-bucket-123",
                "region": "us-east-1",
                "dry_run": False,
            },
            context(),
        )
        self.assertEqual(output["status"], "completed")
        s3.put_public_access_block.assert_called_once()

    @patch.object(contain, "capture_bucket_public_access")
    @patch.object(contain, "bucket_region", return_value="us-east-1")
    @patch.object(contain.boto3, "client")
    def test_containment_is_idempotent(self, client, _region, capture):
        current = dict(BASE_STATE)
        current["public_access_block"] = {
            "present": True,
            "configuration": BLOCK_ALL_PUBLIC_ACCESS,
        }
        capture.return_value = current
        s3 = MagicMock()
        client.side_effect = client_router(s3=s3, sts=sts())
        output = contain.handler(
            {
                "incident_id": "INC-1",
                "bucket_name": "incident-bucket-123",
                "region": "us-east-1",
                "dry_run": False,
            },
            context(),
        )
        self.assertEqual(output["status"], "no_change")
        s3.put_public_access_block.assert_not_called()

    @patch.object(restore, "capture_bucket_public_access")
    @patch.object(restore, "bucket_region", return_value="us-east-1")
    @patch.object(restore.boto3, "client")
    def test_restore_deletes_block_when_originally_absent(self, client, _region, capture):
        capture.return_value = {
            **BASE_STATE,
            "public_access_block": {
                "present": True,
                "configuration": BLOCK_ALL_PUBLIC_ACCESS,
            },
        }
        manifest = create_manifest(
            action="contain_s3_public_access",
            incident_id="INC-1",
            resource_type="s3-bucket",
            resource_id="incident-bucket-123",
            account_id="111122223333",
            region="us-east-1",
            state=BASE_STATE,
        )
        s3 = MagicMock()
        client.side_effect = client_router(s3=s3, sts=sts())
        output = restore.handler(
            {
                "incident_id": "INC-1",
                "bucket_name": "incident-bucket-123",
                "region": "us-east-1",
                "dry_run": False,
                "confirm_restore": True,
                "rollback_manifest": manifest,
            },
            context(),
        )
        self.assertEqual(output["status"], "completed")
        s3.delete_public_access_block.assert_called_once()


if __name__ == "__main__":
    unittest.main()
