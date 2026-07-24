#!/usr/bin/env python3
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for p in sorted(root.rglob("*.json")):
    json.loads(p.read_text())
    print(f"OK {p.relative_to(root)}")
