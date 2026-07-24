import importlib.util, sys, unittest
from pathlib import Path
from unittest.mock import MagicMock, patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"shared"))
spec=importlib.util.spec_from_file_location("disable",ROOT/"lambda"/"disable_iam_access_key"/"app.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class TestDisable(unittest.TestCase):
    @patch.object(mod.boto3,"client")
    def test_dry_run(self,client):
        iam=MagicMock(); client.return_value=iam; iam.get_access_key_last_used.return_value={"AccessKeyLastUsed":{}}
        out=mod.handler({"incident_id":"INC-2","user_name":"u","access_key_id":"AKIAIOSFODNN7EXAMPLE","dry_run":True},MagicMock())
        self.assertEqual(out["status"],"planned"); iam.update_access_key.assert_not_called()
if __name__=="__main__": unittest.main()
