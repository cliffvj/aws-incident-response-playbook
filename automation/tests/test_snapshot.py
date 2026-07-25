import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from helpers import client_router, context, load_action, sts

mod = load_action("snapshot_ebs_volumes")


class TestSnapshot(unittest.TestCase):
    def ec2(self):
        ec2 = MagicMock()
        ec2.describe_instances.return_value = {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "BlockDeviceMappings": [
                                {"Ebs": {"VolumeId": "vol-0123456789abcdef0"}}
                            ]
                        }
                    ]
                }
            ]
        }
        return ec2

    @patch.object(mod.boto3, "client")
    def test_existing_snapshot_prevents_duplicate(self, client):
        ec2 = self.ec2()
        ec2.describe_snapshots.return_value = {
            "Snapshots": [
                {
                    "SnapshotId": "snap-0123456789abcdef0",
                    "State": "completed",
                    "StartTime": "2026-07-24T00:00:00Z",
                }
            ]
        }
        client.side_effect = client_router(ec2=ec2, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-3",
                "instance_id": "i-0123456789abcdef0",
                "region": "us-east-1",
                "dry_run": False,
            },
            context(),
        )
        self.assertEqual(output["status"], "no_change")
        ec2.create_snapshot.assert_not_called()

    @patch.object(mod.boto3, "client")
    def test_create_snapshot(self, client):
        ec2 = self.ec2()
        ec2.describe_snapshots.return_value = {"Snapshots": []}
        ec2.create_snapshot.return_value = {"SnapshotId": "snap-0123456789abcdef0"}
        client.side_effect = client_router(ec2=ec2, sts=sts())
        output = mod.handler(
            {
                "incident_id": "INC-3",
                "instance_id": "i-0123456789abcdef0",
                "region": "us-east-1",
                "dry_run": False,
            },
            context(),
        )
        self.assertEqual(output["status"], "submitted")
        ec2.create_snapshot.assert_called_once()


if __name__ == "__main__":
    unittest.main()
