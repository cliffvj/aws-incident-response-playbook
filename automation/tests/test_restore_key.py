import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from aws_ir.manifests import create_manifest
from helpers import client_router, context, load_action, sts

mod = load_action("restore_iam_access_key")


class TestRestoreKey(unittest.TestCase):
    @patch.object(mod.boto3, "client")
    def test_restore_dry_run(self, client):
        iam = MagicMock()
        iam.list_access_keys.return_value = {
            "AccessKeyMetadata": [
                {
                    "UserName": "analyst",
                    "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
                    "Status": "Inactive",
                }
            ]
        }
        client.side_effect = client_router(iam=iam, sts=sts())
        manifest = create_manifest(
            action="disable_iam_access_key",
            incident_id="INC-2",
            resource_type="iam-access-key",
            resource_id="AKIAIOSFODNN7EXAMPLE",
            account_id="111122223333",
            region="global",
            state={"user_name": "analyst", "status": "Active"},
        )
        output = mod.handler(
            {
                "incident_id": "INC-2",
                "user_name": "analyst",
                "access_key_id": "AKIAIOSFODNN7EXAMPLE",
                "dry_run": True,
                "confirm_restore": True,
                "rollback_manifest": manifest,
            },
            context(),
        )
        self.assertEqual(output["status"], "planned")
        iam.update_access_key.assert_not_called()


if __name__ == "__main__":
    unittest.main()
