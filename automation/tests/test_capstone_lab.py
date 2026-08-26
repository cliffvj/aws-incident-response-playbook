from pathlib import Path
import importlib.util, unittest
ROOT=Path(__file__).resolve().parents[2]
SCRIPT=ROOT/'labs'/'phase3-capstone'/'scripts'/'prepare_lab_inputs.py'
spec=importlib.util.spec_from_file_location('prepare_lab_inputs',SCRIPT); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
class CapstoneLabTests(unittest.TestCase):
    def test_hash_is_deterministic(self):
        seed={'source':'aws-ir.lab','detail_type':'Simulated Security Finding','finding_id':'phase3-capstone-simulated-001','resource_id':'i-0123456789abcdef0'}
        self.assertEqual(module.stable_hash(seed),module.stable_hash(dict(seed)))
    def test_lab_has_no_ingress(self):
        t=(ROOT/'labs'/'phase3-capstone'/'terraform'/'main.tf').read_text(); self.assertNotIn('ingress {',t); self.assertIn('source         = ["aws-ir.lab"]',t); self.assertIn('http_tokens   = "required"',t)
    def test_generated_ignored(self):
        lines=(ROOT/'labs'/'phase3-capstone'/'generated'/'.gitignore').read_text().splitlines(); self.assertIn('*',lines); self.assertIn('!.gitignore',lines)
if __name__=='__main__': unittest.main()
