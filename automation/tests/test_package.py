import subprocess, sys, unittest, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestPackage(unittest.TestCase):
    def test_archives_contain_handler_and_shared(self):
        subprocess.run([sys.executable,str(ROOT/"scripts"/"package_lambdas.py")],check=True)
        for archive in (ROOT/"build").glob("*.zip"):
            with zipfile.ZipFile(archive) as zf:
                names=set(zf.namelist()); self.assertIn("app.py",names); self.assertIn("aws_ir/validation.py",names)
if __name__=="__main__": unittest.main()
