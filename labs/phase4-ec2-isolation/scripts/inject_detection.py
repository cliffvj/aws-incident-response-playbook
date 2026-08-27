#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import boto3


def main() -> int:
    parser = argparse.ArgumentParser(description="Inject one authorized Phase 4 simulated EventBridge finding.")
    parser.add_argument("--detail-file", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--event-bus-name", default="default")
    args = parser.parse_args()

    detail = json.loads(Path(args.detail_file).read_text(encoding="utf-8"))
    if detail.get("simulation") is not True or detail.get("scenario") != "phase4-ec2-isolation":
        raise SystemExit("detail file is not an authorized phase4-ec2-isolation simulation")

    client = boto3.client("events", region_name=args.region)
    response = client.put_events(
        Entries=[
            {
                "Source": "aws-ir.lab",
                "DetailType": "Simulated Security Finding",
                "Detail": json.dumps(detail, separators=(",", ":")),
                "EventBusName": args.event_bus_name,
            }
        ]
    )
    if response.get("FailedEntryCount", 0) != 0:
        entry = (response.get("Entries") or [{}])[0]
        raise SystemExit(f"EventBridge PutEvents failed: {entry.get('ErrorCode')} {entry.get('ErrorMessage')}")

    event_id = (response.get("Entries") or [{}])[0].get("EventId", "")
    print(f"OK: EventBridge accepted simulated finding event_id={event_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
