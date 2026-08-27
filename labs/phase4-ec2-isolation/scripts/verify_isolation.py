#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re

import boto3

INCIDENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,63}$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify incident-specific EC2 security-group quarantine.")
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--incident-id", required=True)
    parser.add_argument("--region", required=True)
    args = parser.parse_args()

    if not INCIDENT.fullmatch(args.incident_id):
        raise SystemExit("invalid --incident-id")

    expected_name = f"aws-ir-quarantine-{args.incident_id}"
    ec2 = boto3.client("ec2", region_name=args.region)
    response = ec2.describe_network_interfaces(
        Filters=[{"Name": "attachment.instance-id", "Values": [args.instance_id]}]
    )
    enis = response.get("NetworkInterfaces", [])
    if not enis:
        raise SystemExit("ERROR: no network interfaces found for target")

    for eni in enis:
        groups = eni.get("Groups", [])
        names = [g.get("GroupName") for g in groups]
        if names != [expected_name]:
            raise SystemExit(f"ERROR: {eni.get('NetworkInterfaceId')} is not isolated: {names}")

    print(f"OK: all {len(enis)} target network interface(s) use only {expected_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
