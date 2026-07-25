#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "action-catalog.json").read_text(encoding="utf-8"))

listed = {item["name"] for item in CATALOG["actions"]}
actual = {path.name for path in (ROOT / "lambda").iterdir() if path.is_dir()}
errors: list[str] = []

for missing in sorted(listed - actual):
    errors.append(f"catalog action has no Lambda directory: {missing}")
for unlisted in sorted(actual - listed):
    errors.append(f"Lambda directory is absent from catalog: {unlisted}")

for item in CATALOG["actions"]:
    action_dir = ROOT / "lambda" / item["name"]
    for required in ("app.py", "README.md"):
        if not (action_dir / required).is_file():
            errors.append(f"{item['name']} is missing {required}")
    for sample in item.get("sample_events", []):
        if not (ROOT / "samples" / sample).is_file():
            errors.append(f"{item['name']} sample does not exist: {sample}")
    for runbook in item.get("runbooks", []):
        if not (ROOT / runbook).resolve().is_file():
            errors.append(f"{item['name']} runbook does not exist: {runbook}")
    rollback = item.get("rollback_action")
    if rollback and rollback not in listed:
        errors.append(f"{item['name']} has unknown rollback action: {rollback}")

if errors:
    for error in errors:
        print(f"ERROR: {error}")
    raise SystemExit(1)

print(f"OK: validated {len(listed)} action contracts")
