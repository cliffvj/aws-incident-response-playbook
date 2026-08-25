#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "detection" / "event-patterns"
SAMPLES = ROOT / "detection" / "samples"

required = {
    "guardduty-medium-high.json": ("aws.guardduty", "GuardDuty Finding"),
    "securityhub-findings.json": ("aws.securityhub", "Security Hub Findings - Imported"),
    "config-noncompliant.json": ("aws.config", "Config Rules Compliance Change"),
    "cloudwatch-alarm.json": ("aws.cloudwatch", "CloudWatch Alarm State Change"),
    "cloudtrail-trail-tampering.json": ("aws.cloudtrail", "AWS API Call via CloudTrail"),
}
errors=[]
for name,(source,detail_type) in required.items():
    path=PATTERNS/name
    if not path.is_file():
        errors.append(f"missing event pattern: {name}")
        continue
    value=json.loads(path.read_text(encoding="utf-8"))
    if source not in value.get("source",[]): errors.append(f"{name}: source mismatch")
    if detail_type not in value.get("detail-type",[]): errors.append(f"{name}: detail-type mismatch")

for path in sorted(SAMPLES.glob("*.json")):
    value=json.loads(path.read_text(encoding="utf-8"))
    for key in ("id","source","detail-type","account","region","detail"):
        if key not in value: errors.append(f"{path.name}: missing {key}")

if errors:
    print("\n".join(f"ERROR: {x}" for x in errors)); raise SystemExit(1)
print(f"OK: validated {len(required)} EventBridge patterns and {len(list(SAMPLES.glob('*.json')))} detection samples")
