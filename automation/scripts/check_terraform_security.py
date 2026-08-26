#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"terraform"
errors=[]
for path in ROOT.rglob("*.tf"):
    text=path.read_text(encoding="utf-8")
    lowered=text.lower()
    if re.search(r'acl\s*=\s*"public-read"', lowered):
        errors.append(f"{path}: public-read ACL is forbidden")
    if "0.0.0.0/0" in text and "/examples/" not in path.as_posix():
        errors.append(f"{path}: internet-wide CIDR outside an explicit example")
notifications=(ROOT/"modules"/"notifications"/"main.tf").read_text(encoding="utf-8")
if not re.search(r"kms_master_key_id\s*=", notifications):
    errors.append("notifications module must encrypt SNS topics")
investigation=(ROOT/"modules"/"investigation"/"main.tf").read_text(encoding="utf-8")
for key in ("block_public_acls","block_public_policy","ignore_public_acls","restrict_public_buckets"):
    if not re.search(rf"{key}\s*=\s*true", investigation):
        errors.append(f"investigation module missing safety setting: {key}=true")
if not re.search(r'sse_algorithm\s*=\s*"aws:kms"', investigation):
    errors.append("investigation module missing SSE-KMS configuration")
if errors:
    print("\n".join("ERROR: "+e for e in errors)); raise SystemExit(1)
print(f"OK: Terraform security-oriented static checks passed across {len(list(ROOT.rglob('*.tf')))} files")
