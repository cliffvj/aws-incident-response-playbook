import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import client_router, context, load_action, sts

mod = load_action("isolate_ec2_instance")


class TestIsolate(unittest.TestCase):
    def setUp(self):
        self.ec2 = MagicMock()
        self.ec2.describe_instances.return_value = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "VpcId": "vpc-0123456789abcdef0",
                            "NetworkInterfaces": [
                                {
                                    "NetworkInterfaceId": "eni-0123456789abcdef0",
                                    "Groups": [{"GroupId": "sg-01111111111111111"}],
                                },
                                {
                                    "NetworkInterfaceId": "eni-02222222222222222",
                                    "Groups": [{"GroupId": "sg-02222222222222222"}],
                                },
                            ],
                        }
                    ]
                }
            ]
        }
        self.ec2.describe_security_groups.return_value = {
            "SecurityGroups": [
                {
                    "GroupId": "sg-09999999999999999",
                    "VpcId": "vpc-0123456789abcdef0",
                    "IpPermissions": [],
                    "IpPermissionsEgress": [],
                }
            ]
        }

    @patch.object(mod.boto3, "client")
    def test_dry_run_does_not_modify(self, client):
        client.side_effect = client_router(ec2=self.ec2, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-1",
                "instance_id": "i-0123456789abcdef0",
                "quarantine_security_group_id": "sg-09999999999999999",
                "region": "us-east-1",
                "dry_run": True,
            },
            context(),
        )
        self.assertEqual(output["status"], "planned")
        self.assertIn("rollback_manifest", output["details"])
        self.ec2.modify_network_interface_attribute.assert_not_called()

    @patch.object(mod.boto3, "client")
    def test_execute_changes_each_interface(self, client):
        client.side_effect = client_router(ec2=self.ec2, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-1",
                "instance_id": "i-0123456789abcdef0",
                "quarantine_security_group_id": "sg-09999999999999999",
                "region": "us-east-1",
                "dry_run": False,
            },
            context(),
        )
        self.assertEqual(output["status"], "completed")
        self.assertEqual(self.ec2.modify_network_interface_attribute.call_count, 2)

    @patch.object(mod.boto3, "client")
    def test_idempotent_when_already_isolated(self, client):
        for interface in self.ec2.describe_instances.return_value["Reservations"][0]["Instances"][0]["NetworkInterfaces"]:
            interface["Groups"] = [{"GroupId": "sg-09999999999999999"}]
        client.side_effect = client_router(ec2=self.ec2, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-1",
                "instance_id": "i-0123456789abcdef0",
                "quarantine_security_group_id": "sg-09999999999999999",
                "region": "us-east-1",
                "dry_run": False,
            },
            context(),
        )
        self.assertEqual(output["status"], "no_change")
        self.ec2.modify_network_interface_attribute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
