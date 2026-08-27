#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

INSTANCE = re.compile(r"^i-[0-9a-f]{8,17}$")
ACCOUNT = re.compile(r"^\d{12}$")
REGION = re.compile(r"^[a-z]{2}(?:-gov)?-[a-z]+-\d$")


def stable_hash(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_inputs(*, instance_id: str, account_id: str, region: str, requested_by: str, finding_id: str) -> dict[str, object]:
    if not INSTANCE.fullmatch(instance_id):
        raise ValueError("invalid instance_id")
    if not ACCOUNT.fullmatch(account_id):
        raise ValueError("invalid account_id")
    if not REGION.fullmatch(region):
        raise ValueError("invalid region")
    if not requested_by.strip():
        raise ValueError("requested_by is required")
    if not finding_id.strip():
        raise ValueError("finding_id is required")

    seed = {
        "source": "aws-ir.lab",
        "detail_type": "Simulated Security Finding",
        "finding_id": finding_id,
        "resource_id": instance_id,
    }
    dedupe_key = stable_hash(seed)
    incident_id = f"EVT-{dedupe_key[:20]}"

    detail = {
        "finding_id": finding_id,
        "severity": "HIGH",
        "title": "Authorized Phase 4 EC2 compromise simulation",
        "instance_id": instance_id,
        "simulation": True,
        "scenario": "phase4-ec2-isolation",
    }
    containment = {
        "event_id": f"phase4-ec2-contain-{dedupe_key[:32]}",
        "incident_id": incident_id,
        "mode": "containment",
        "expected_account_id": account_id,
        "region": region,
        "instance_id": instance_id,
        "requested_by": requested_by,
        "reason": "Authorized Phase 4 EC2 compromise and isolation practice lab",
        "severity": "HIGH",
        "dry_run": False,
    }
    context = {
        "schema": "aws-ir-practice-lab-context/v1",
        "scenario": "phase4-ec2-isolation",
        "incident_id": incident_id,
        "finding_id": finding_id,
        "instance_id": instance_id,
        "account_id": account_id,
        "region": region,
        "requested_by": requested_by,
        "dedupe_key": dedupe_key,
    }
    return {"incident_id": incident_id, "detail": detail, "containment": containment, "context": context}


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare deterministic Phase 4 EC2 isolation lab inputs.")
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--requested-by", required=True)
    parser.add_argument("--finding-id", default="phase4-ec2-isolation-simulated-001")
    parser.add_argument("--output-dir", default="labs/phase4-ec2-isolation/generated")
    args = parser.parse_args()

    try:
        values = build_inputs(
            instance_id=args.instance_id,
            account_id=args.account_id,
            region=args.region,
            requested_by=args.requested_by,
            finding_id=args.finding_id,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "event-detail.json").write_text(json.dumps(values["detail"], indent=2) + "\n", encoding="utf-8")
    (out / "containment-live.json").write_text(json.dumps(values["containment"], indent=2) + "\n", encoding="utf-8")
    (out / "scenario-context.json").write_text(json.dumps(values["context"], indent=2) + "\n", encoding="utf-8")
    (out / "incident-id.txt").write_text(str(values["incident_id"]) + "\n", encoding="utf-8")

    print(f"incident_id={values['incident_id']}")
    print(f"event_detail={out / 'event-detail.json'}")
    print(f"containment_input={out / 'containment-live.json'}")
    print(f"scenario_context={out / 'scenario-context.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
