import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"shared"))
from aws_ir.validation import dry_run, require_string
from aws_ir.errors import ValidationError
class TestValidation(unittest.TestCase):
    def test_dry_run_defaults_true(self): self.assertTrue(dry_run({}))
    def test_dry_run_false(self): self.assertFalse(dry_run({"dry_run":False}))
    def test_reject_non_boolean(self):
        with self.assertRaises(ValidationError): dry_run({"dry_run":"false"})
    def test_require_string(self): self.assertEqual(require_string({"x":" value "},"x"),"value")
if __name__=="__main__": unittest.main()
