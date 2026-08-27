#!/usr/bin/env python3
from __future__ import annotations

import argparse

import boto3


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Phase 4 EC2 target safety preconditions.")
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--region", required=True)
    args = parser.parse_args()

    ec2 = boto3.client("ec2", region_name=args.region)
    ssm = boto3.client("ssm", region_name=args.region)

    response = ec2.describe_instances(InstanceIds=[args.instance_id])
    instances = [i for r in response.get("Reservations", []) for i in r.get("Instances", [])]
    if len(instances) != 1:
        raise SystemExit("ERROR: target instance was not uniquely returned")
    instance = instances[0]

    if instance.get("MetadataOptions", {}).get("HttpTokens") != "required":
        raise SystemExit("ERROR: target does not require IMDSv2")

    mappings = instance.get("BlockDeviceMappings", [])
    if not mappings:
        raise SystemExit("ERROR: target has no EBS block-device mapping")
    volume_ids = [m.get("Ebs", {}).get("VolumeId") for m in mappings if m.get("Ebs", {}).get("VolumeId")]
    volumes = ec2.describe_volumes(VolumeIds=volume_ids).get("Volumes", [])
    if not volumes or any(v.get("Encrypted") is not True for v in volumes):
        raise SystemExit("ERROR: one or more target EBS volumes are not encrypted")

    group_ids = [g["GroupId"] for g in instance.get("SecurityGroups", [])]
    groups = ec2.describe_security_groups(GroupIds=group_ids).get("SecurityGroups", [])
    if any(g.get("IpPermissions") for g in groups):
        raise SystemExit("ERROR: target security group has inbound permissions")

    info = ssm.describe_instance_information(Filters=[{"Key": "InstanceIds", "Values": [args.instance_id]}])
    nodes = info.get("InstanceInformationList", [])
    if len(nodes) != 1 or nodes[0].get("PingStatus") != "Online":
        raise SystemExit("ERROR: target is not Online in Systems Manager")

    print("OK: target is encrypted, IMDSv2-required, no-ingress, and Online in Systems Manager")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
