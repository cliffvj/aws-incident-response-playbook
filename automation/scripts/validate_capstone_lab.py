#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import re

ROOT=Path(__file__).resolve().parents[2]
LAB=ROOT/'labs'/'phase3-capstone'
required=[LAB/'README.md',LAB/'troubleshooting.md',LAB/'terraform'/'main.tf',LAB/'terraform'/'variables.tf',LAB/'terraform'/'outputs.tf',LAB/'scripts'/'prepare_lab_inputs.py',LAB/'scripts'/'inject_detection.sh',LAB/'scripts'/'verify_isolation.sh',LAB/'scripts'/'extract_rollback_input.py']
for p in required:
    if not p.exists(): raise SystemExit(f"missing capstone file: {p.relative_to(ROOT)}")
text=(LAB/'terraform'/'main.tf').read_text()
checks = {
    "capstone target must not define inbound security-group rules":
        re.search(r"\bingress\s*\{", text) is None,

    "EventBridge rule must be lab-scoped":
        re.search(r'source\s*=\s*\["aws-ir\.lab"\]', text) is not None,

    "simulated detail type missing":
        '"Simulated Security Finding"' in text,

    "IMDSv2 tokens must be required":
        re.search(r'http_tokens\s*=\s*"required"', text) is not None,

    "root EBS must be encrypted":
        re.search(r"encrypted\s*=\s*true", text) is not None,
}
for msg,ok in checks.items():
    if not ok: raise SystemExit(msg)
for forbidden in ['msfvenom','meterpreter','reverse shell','security-credentials/']:
    if forbidden.lower() in text.lower(): raise SystemExit(f"forbidden offensive lab content: {forbidden}")
lines=(LAB/'generated'/'.gitignore').read_text().splitlines()
if '*' not in lines or '!.gitignore' not in lines: raise SystemExit('generated runtime files must be ignored by Git')
with tempfile.TemporaryDirectory() as td:
    subprocess.run(
    [
        sys.executable,
        str(LAB / "scripts" / "prepare_lab_inputs.py"),
        "--instance-id",
        "i-0123456789abcdef0",
        "--account-id",
        "111122223333",
        "--region",
        "us-east-1",
        "--requested-by",
        "validator",
        "--output-dir",
        td,
    ],
    check=True,
    capture_output=True,
    text=True,
    )
    c=json.loads((Path(td)/'containment-live.json').read_text()); d=json.loads((Path(td)/'event-detail.json').read_text())
    if c.get('dry_run') is not False or c.get('mode') != 'containment': raise SystemExit('capstone containment input malformed')
    if d.get('simulation') is not True: raise SystemExit('capstone event must be explicitly simulated')
print('OK: Phase 3 capstone lab structure and safety checks passed')
