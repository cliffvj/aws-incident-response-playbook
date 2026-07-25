from __future__ import annotations

import boto3

from aws_ir.context import region_from, same_account_id
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.validation import require_incident, require_instance_id


def handler(event, context):
    incident_id = require_incident(event)
    instance_id = require_instance_id(event)
    region = region_from(event)
    account_id = same_account_id(event, boto3.client("sts"))

    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances(InstanceIds=[instance_id])
    reservations = response.get("Reservations", [])
    if not reservations or not reservations[0].get("Instances"):
        raise ValueError(f"instance not found: {instance_id}")

    instance = reservations[0]["Instances"][0]
    details = {
        "account_id": account_id,
        "instance_id": instance_id,
        "region": region,
        "state": instance.get("State", {}).get("Name"),
        "vpc_id": instance.get("VpcId"),
        "subnet_id": instance.get("SubnetId"),
        "security_groups": instance.get("SecurityGroups", []),
        "network_interfaces": [
            {
                "id": interface.get("NetworkInterfaceId"),
                "private_ip": interface.get("PrivateIpAddress"),
                "groups": interface.get("Groups", []),
            }
            for interface in instance.get("NetworkInterfaces", [])
        ],
        "volumes": [
            mapping.get("Ebs", {}).get("VolumeId")
            for mapping in instance.get("BlockDeviceMappings", [])
            if mapping.get("Ebs")
        ],
        "iam_instance_profile": instance.get("IamInstanceProfile"),
        "tags": instance.get("Tags", []),
        "launch_time": instance.get("LaunchTime"),
    }
    log(
        "ec2_metadata_collected",
        incident_id=incident_id,
        instance_id=instance_id,
        account_id=account_id,
        region=region,
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="collect_ec2_metadata",
        incident_id=incident_id,
        dry_run=True,
        status="observed",
        details=details,
    )
