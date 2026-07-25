from __future__ import annotations

import boto3

from aws_ir.context import region_from, same_account_id
from aws_ir.logging import log
from aws_ir.manifests import create_manifest
from aws_ir.response import result
from aws_ir.validation import (
    dry_run,
    require_incident,
    require_instance_id,
    require_security_group_id,
)


def _instance(ec2, instance_id: str) -> dict:
    response = ec2.describe_instances(InstanceIds=[instance_id])
    reservations = response.get("Reservations", [])
    if not reservations or not reservations[0].get("Instances"):
        raise ValueError(f"instance not found: {instance_id}")
    return reservations[0]["Instances"][0]


def handler(event, context):
    incident_id = require_incident(event)
    instance_id = require_instance_id(event)
    quarantine_sg = require_security_group_id(event)
    is_dry = dry_run(event)
    region = region_from(event)
    account_id = same_account_id(event, boto3.client("sts"))

    ec2 = boto3.client("ec2", region_name=region)
    instance = _instance(ec2, instance_id)
    vpc_id = instance.get("VpcId")
    interfaces = instance.get("NetworkInterfaces", [])
    if not interfaces:
        raise ValueError("instance has no network interfaces to isolate")

    security_group = ec2.describe_security_groups(GroupIds=[quarantine_sg]).get(
        "SecurityGroups", []
    )
    if not security_group:
        raise ValueError(f"security group not found: {quarantine_sg}")
    if security_group[0].get("VpcId") != vpc_id:
        raise ValueError("quarantine security group must be in the instance VPC")
    if security_group[0].get("IpPermissions") or security_group[0].get(
        "IpPermissionsEgress"
    ):
        raise ValueError("quarantine security group must have no ingress or egress rules")

    interface_state = [
        {
            "network_interface_id": interface["NetworkInterfaceId"],
            "security_group_ids": [group["GroupId"] for group in interface.get("Groups", [])],
        }
        for interface in interfaces
    ]
    manifest = create_manifest(
        action="isolate_ec2_instance",
        incident_id=incident_id,
        resource_type="ec2-instance",
        resource_id=instance_id,
        account_id=account_id,
        region=region,
        state={"network_interfaces": interface_state},
        metadata={"quarantine_security_group_id": quarantine_sg},
    )

    pending = [
        interface
        for interface in interface_state
        if interface["security_group_ids"] != [quarantine_sg]
    ]
    details = {
        "account_id": account_id,
        "instance_id": instance_id,
        "vpc_id": vpc_id,
        "region": region,
        "quarantine_security_group_id": quarantine_sg,
        "interfaces": interface_state,
        "interfaces_requiring_change": [
            interface["network_interface_id"] for interface in pending
        ],
        "rollback_manifest": manifest,
    }

    if not pending:
        return result(
            action="isolate_ec2_instance",
            incident_id=incident_id,
            dry_run=is_dry,
            status="no_change",
            details=details,
        )
    if is_dry:
        log("ec2_isolation_planned", incident_id=incident_id, **details)
        return result(
            action="isolate_ec2_instance",
            incident_id=incident_id,
            dry_run=True,
            status="planned",
            details=details,
        )

    changed = []
    for interface in pending:
        ec2.modify_network_interface_attribute(
            NetworkInterfaceId=interface["network_interface_id"],
            Groups=[quarantine_sg],
        )
        changed.append(interface["network_interface_id"])
    details["changed_network_interface_ids"] = changed
    log(
        "ec2_isolated",
        incident_id=incident_id,
        instance_id=instance_id,
        network_interface_ids=changed,
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="isolate_ec2_instance",
        incident_id=incident_id,
        dry_run=False,
        status="completed",
        details=details,
    )
