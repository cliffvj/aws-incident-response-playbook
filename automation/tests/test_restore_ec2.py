import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from aws_ir.manifests import create_manifest
from helpers import client_router, context, load_action, sts

mod = load_action("restore_ec2_security_groups")


class TestRestoreEc2(unittest.TestCase):
    def manifest(self):
        return create_manifest(
            action="isolate_ec2_instance",
            incident_id="INC-1",
            resource_type="ec2-instance",
            resource_id="i-0123456789abcdef0",
            account_id="111122223333",
            region="us-east-1",
            state={
                "network_interfaces": [
                    {
                        "network_interface_id": "eni-0123456789abcdef0",
                        "security_group_ids": ["sg-01111111111111111"],
                    }
                ]
            },
        )

    @patch.object(mod.boto3, "client")
    def test_dry_run_restore(self, client):
        ec2 = MagicMock()
        ec2.describe_network_interfaces.return_value = {
            "NetworkInterfaces": [
                {
                    "NetworkInterfaceId": "eni-0123456789abcdef0",
                    "Groups": [{"GroupId": "sg-09999999999999999"}],
                }
            ]
        }
        client.side_effect = client_router(ec2=ec2, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-1",
                "instance_id": "i-0123456789abcdef0",
                "region": "us-east-1",
                "dry_run": True,
                "confirm_restore": True,
                "rollback_manifest": self.manifest(),
            },
            context(),
        )
        self.assertEqual(output["status"], "planned")
        ec2.modify_network_interface_attribute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
