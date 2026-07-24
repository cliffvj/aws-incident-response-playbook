import importlib.util, sys, unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"shared"))
spec=importlib.util.spec_from_file_location("isolate",ROOT/"lambda"/"isolate_ec2_instance"/"app.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class TestIsolate(unittest.TestCase):
    @patch.object(mod.boto3,"client")
    def test_dry_run_does_not_modify(self,client):
        ec2=MagicMock(); client.return_value=ec2
        ec2.describe_instances.return_value={"Reservations":[{"Instances":[{"VpcId":"vpc-1","SecurityGroups":[{"GroupId":"sg-old"}]}]}]}
        ec2.describe_security_groups.return_value={"SecurityGroups":[{"GroupId":"sg-q","VpcId":"vpc-1"}]}
        out=mod.handler({"incident_id":"INC-1","instance_id":"i-1","quarantine_security_group_id":"sg-q","dry_run":True},MagicMock())
        self.assertEqual(out["status"],"planned"); ec2.modify_instance_attribute.assert_not_called()
if __name__=="__main__": unittest.main()
