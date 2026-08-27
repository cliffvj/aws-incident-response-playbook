#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time

import boto3


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a harmless suspicious-activity marker through SSM Run Command.")
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--region", required=True)
    parser.add_argument("--wait-seconds", type=int, default=90)
    args = parser.parse_args()

    ssm = boto3.client("ssm", region_name=args.region)
    response = ssm.send_command(
        InstanceIds=[args.instance_id],
        DocumentName="AWS-RunShellScript",
        Comment="Authorized Phase 4 EC2 compromise simulation: marker file only",
        Parameters={
            "commands": [
                "set -eu",
                "mkdir -p /var/tmp/aws-ir-practice",
                "printf '%s\\n' 'AUTHORIZED AWS INCIDENT RESPONSE PRACTICE LAB' > /var/tmp/aws-ir-practice/simulated-suspicious-activity.txt",
                "printf '%s\\n' 'Benign marker only: no malware, exploit, persistence, credential access, or exfiltration.' >> /var/tmp/aws-ir-practice/simulated-suspicious-activity.txt",
                "date -u '+created_utc=%Y-%m-%dT%H:%M:%SZ' >> /var/tmp/aws-ir-practice/simulated-suspicious-activity.txt",
                "chmod 0644 /var/tmp/aws-ir-practice/simulated-suspicious-activity.txt",
                "stat /var/tmp/aws-ir-practice/simulated-suspicious-activity.txt",
            ]
        },
    )
    command_id = response["Command"]["CommandId"]
    print(f"command_id={command_id}")

    deadline = time.time() + max(0, args.wait_seconds)
    while time.time() < deadline:
        try:
            result = ssm.get_command_invocation(CommandId=command_id, InstanceId=args.instance_id)
        except ssm.exceptions.InvocationDoesNotExist:
            time.sleep(2)
            continue
        status = result.get("Status", "")
        if status in {"Success", "Cancelled", "TimedOut", "Failed", "Cancelling"}:
            if status != "Success":
                raise SystemExit(f"SSM simulation command ended with status={status}: {result.get('StandardErrorContent', '')}")
            print("OK: benign suspicious-activity marker created")
            if result.get("StandardOutputContent"):
                print(result["StandardOutputContent"].strip())
            return 0
        time.sleep(2)

    raise SystemExit(f"timed out waiting for SSM command {command_id}")


if __name__ == "__main__":
    raise SystemExit(main())
