import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import client_router, context, load_action, sts

mod = load_action("ensure_quarantine_security_group")


class TestQuarantineGroup(unittest.TestCase):
    @patch.object(mod.boto3, "client")
    def test_dry_run_plans_creation(self, client):
        ec2 = MagicMock()
        ec2.describe_security_groups.return_value = {"SecurityGroups": []}
        client.side_effect = client_router(ec2=ec2, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-1",
                "vpc_id": "vpc-0123456789abcdef0",
                "region": "us-east-1",
                "dry_run": True,
            },
            context(),
        )
        self.assertEqual(output["status"], "planned")
        ec2.create_security_group.assert_not_called()

    @patch.object(mod.boto3, "client")
    def test_existing_ruleless_group_is_reused(self, client):
        ec2 = MagicMock()
        ec2.describe_security_groups.return_value = {
            "SecurityGroups": [
                {
                    "GroupId": "sg-09999999999999999",
                    "IpPermissions": [],
                    "IpPermissionsEgress": [],
                }
            ]
        }
        client.side_effect = client_router(ec2=ec2, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-1",
                "vpc_id": "vpc-0123456789abcdef0",
                "region": "us-east-1",
                "dry_run": False,
            },
            context(),
        )
        self.assertEqual(output["status"], "no_change")
        self.assertTrue(output["details"]["reused"])

    @patch.object(mod.boto3, "client")
    def test_create_removes_default_egress(self, client):
        ec2 = MagicMock()
        ec2.describe_security_groups.side_effect = [
            {"SecurityGroups": []},
            {
                "SecurityGroups": [
                    {
                        "GroupId": "sg-09999999999999999",
                        "IpPermissions": [],
                        "IpPermissionsEgress": [
                            {"IpProtocol": "-1", "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}
                        ],
                    }
                ]
            },
            {
                "SecurityGroups": [
                    {
                        "GroupId": "sg-09999999999999999",
                        "IpPermissions": [],
                        "IpPermissionsEgress": [],
                    }
                ]
            },
        ]
        ec2.create_security_group.return_value = {"GroupId": "sg-09999999999999999"}
        client.side_effect = client_router(ec2=ec2, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-1",
                "vpc_id": "vpc-0123456789abcdef0",
                "region": "us-east-1",
                "dry_run": False,
            },
            context(),
        )
        self.assertEqual(output["status"], "completed")
        ec2.revoke_security_group_egress.assert_called_once()


if __name__ == "__main__":
    unittest.main()
