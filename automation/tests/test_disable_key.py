import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import client_router, context, load_action, sts

mod = load_action("disable_iam_access_key")


class TestDisable(unittest.TestCase):
    def iam(self, status="Active"):
        iam = MagicMock()
        iam.list_access_keys.return_value = {
            "AccessKeyMetadata": [
                {
                    "UserName": "analyst",
                    "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
                    "Status": status,
                }
            ]
        }
        iam.get_access_key_last_used.return_value = {"AccessKeyLastUsed": {}}
        return iam

    @patch.object(mod.boto3, "client")
    def test_dry_run(self, client):
        iam = self.iam()
        client.side_effect = client_router(iam=iam, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-2",
                "user_name": "analyst",
                "access_key_id": "AKIAIOSFODNN7EXAMPLE",
                "dry_run": True,
            },
            context(),
        )
        self.assertEqual(output["status"], "planned")
        self.assertIn("rollback_manifest", output["details"])
        iam.update_access_key.assert_not_called()

    @patch.object(mod.boto3, "client")
    def test_inactive_key_is_no_change(self, client):
        iam = self.iam(status="Inactive")
        client.side_effect = client_router(iam=iam, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-2",
                "user_name": "analyst",
                "access_key_id": "AKIAIOSFODNN7EXAMPLE",
                "dry_run": False,
            },
            context(),
        )
        self.assertEqual(output["status"], "no_change")
        iam.update_access_key.assert_not_called()


if __name__ == "__main__":
    unittest.main()
