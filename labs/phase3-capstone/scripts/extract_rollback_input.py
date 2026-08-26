#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, uuid
from pathlib import Path
from typing import Any
import boto3

def find_manifest(value: Any):
    if isinstance(value, dict):
        if value.get("manifest_version") == 1 and value.get("action") == "isolate_ec2_instance" and value.get("checksum_sha256"):
            return value
        for child in value.values():
            hit=find_manifest(child)
            if hit: return hit
    elif isinstance(value, list):
        for child in value:
            hit=find_manifest(child)
            if hit: return hit
    return None

def main() -> int:
    p=argparse.ArgumentParser(description="Build rollback input from a completed containment execution.")
    p.add_argument("--execution-arn", required=True)
    p.add_argument("--output", default="labs/phase3-capstone/generated/rollback-live.json")
    p.add_argument("--requested-by", default="phase3-capstone-responder")
    a=p.parse_args()
    parts=a.execution_arn.split(":")
    if len(parts) < 7 or parts[2] != "states": raise SystemExit("invalid Step Functions execution ARN")
    client=boto3.client("stepfunctions", region_name=parts[3])
    response=client.describe_execution(executionArn=a.execution_arn)
    if response.get("status") != "SUCCEEDED": raise SystemExit(f"containment execution is not SUCCEEDED: {response.get('status')}")
    output=json.loads(response.get("output") or "{}")
    original=json.loads(response.get("input") or "{}")
    manifest=find_manifest(output)
    if not manifest: raise SystemExit("no checksummed isolate_ec2_instance rollback manifest found")
    resource=manifest.get("resource", {})
    incident_id=original.get("incident_id") or manifest.get("incident_id")
    account_id=original.get("expected_account_id") or resource.get("account_id")
    instance_id=original.get("instance_id") or resource.get("id")
    region=original.get("region") or resource.get("region") or parts[3]
    if not all([incident_id, account_id, instance_id, region]): raise SystemExit("execution output is missing rollback identity context")
    rollback={
        "event_id":f"capstone-rollback-{uuid.uuid4().hex[:32]}", "incident_id":incident_id, "mode":"rollback",
        "expected_account_id":account_id, "region":region, "instance_id":instance_id, "requested_by":a.requested_by,
        "reason":"Authorized Phase 3 capstone network rollback", "severity":original.get("severity","HIGH"), "dry_run":False,
        "confirm_restore":True, "rollback_manifest":manifest,
    }
    path=Path(a.output); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(rollback, indent=2)+"\n", encoding="utf-8")
    print(path); return 0

if __name__ == "__main__": raise SystemExit(main())
