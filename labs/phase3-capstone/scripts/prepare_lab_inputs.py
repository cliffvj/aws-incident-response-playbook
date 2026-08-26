#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

INSTANCE = re.compile(r"^i-[0-9a-f]{8,17}$")
ACCOUNT = re.compile(r"^\d{12}$")


def stable_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare deterministic Phase 3 capstone inputs.")
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--requested-by", required=True)
    parser.add_argument("--finding-id", default="phase3-capstone-simulated-001")
    parser.add_argument("--output-dir", default="labs/phase3-capstone/generated")
    args = parser.parse_args()

    if not INSTANCE.fullmatch(args.instance_id): raise SystemExit("invalid --instance-id")
    if not ACCOUNT.fullmatch(args.account_id): raise SystemExit("invalid --account-id")
    if not args.region.strip(): raise SystemExit("--region is required")
    if not args.requested_by.strip(): raise SystemExit("--requested-by is required")

    seed = {
        "source": "aws-ir.lab",
        "detail_type": "Simulated Security Finding",
        "finding_id": args.finding_id,
        "resource_id": args.instance_id,
    }
    dedupe_key = stable_hash(seed)
    incident_id = f"EVT-{dedupe_key[:20]}"
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)

    detail = {
        "finding_id": args.finding_id,
        "severity": "HIGH",
        "title": "Authorized Phase 3 capstone suspicious-activity simulation",
        "instance_id": args.instance_id,
        "simulation": True,
    }
    containment = {
        "event_id": f"capstone-contain-{dedupe_key[:32]}",
        "incident_id": incident_id,
        "mode": "containment",
        "expected_account_id": args.account_id,
        "region": args.region,
        "instance_id": args.instance_id,
        "requested_by": args.requested_by,
        "reason": "Authorized Phase 3 capstone containment exercise",
        "severity": "HIGH",
        "dry_run": False,
    }
    (out / "event-detail.json").write_text(json.dumps(detail, indent=2) + "\n", encoding="utf-8")
    (out / "containment-live.json").write_text(json.dumps(containment, indent=2) + "\n", encoding="utf-8")
    (out / "incident-id.txt").write_text(incident_id + "\n", encoding="utf-8")
    print(f"incident_id={incident_id}")
    print(f"event_detail={out / 'event-detail.json'}")
    print(f"containment_input={out / 'containment-live.json'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
