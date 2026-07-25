from __future__ import annotations

import re

import boto3
from botocore.exceptions import ClientError

from aws_ir.context import region_from, same_account_id
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.tags import incident_tags
from aws_ir.validation import dry_run, require_incident, require_vpc_id


def _group_name(incident_id: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]", "-", incident_id).strip("-.")
    return f"aws-ir-quarantine-{normalized}"[:255]


def _find_group(ec2, vpc_id: str, group_name: str) -> dict | None:
    response = ec2.describe_security_groups(
        Filters=[
            {"Name": "vpc-id", "Values": [vpc_id]},
            {"Name": "group-name", "Values": [group_name]},
        ]
    )
    groups = response.get("SecurityGroups", [])
    return groups[0] if groups else None


def _validate_ruleless(group: dict) -> None:
    if group.get("IpPermissions") or group.get("IpPermissionsEgress"):
        raise ValueError(
            "existing quarantine security group contains rules; review it manually instead of reusing it"
        )


def handler(event, context):
    incident_id = require_incident(event)
    vpc_id = require_vpc_id(event)
    is_dry = dry_run(event)
    region = region_from(event)
    account_id = same_account_id(event, boto3.client("sts"))
    requested_by = event.get("requested_by")
    group_name = _group_name(incident_id)

    ec2 = boto3.client("ec2", region_name=region)
    existing = _find_group(ec2, vpc_id, group_name)
    if existing:
        _validate_ruleless(existing)
        return result(
            action="ensure_quarantine_security_group",
            incident_id=incident_id,
            dry_run=is_dry,
            status="no_change",
            details={
                "account_id": account_id,
                "region": region,
                "vpc_id": vpc_id,
                "group_id": existing["GroupId"],
                "group_name": group_name,
                "reused": True,
            },
        )

    details = {
        "account_id": account_id,
        "region": region,
        "vpc_id": vpc_id,
        "group_name": group_name,
        "reused": False,
        "planned_rules": {"ingress": [], "egress": []},
    }
    if is_dry:
        return result(
            action="ensure_quarantine_security_group",
            incident_id=incident_id,
            dry_run=True,
            status="planned",
            details=details,
        )

    try:
        response = ec2.create_security_group(
            GroupName=group_name,
            Description=f"Incident-response quarantine group for {incident_id}",
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    "ResourceType": "security-group",
                    "Tags": incident_tags(
                        incident_id,
                        requested_by,
                        action="ensure_quarantine_security_group",
                    ),
                }
            ],
        )
        group_id = response["GroupId"]
    except ClientError as error:
        if error.response.get("Error", {}).get("Code") != "InvalidGroup.Duplicate":
            raise
        existing = _find_group(ec2, vpc_id, group_name)
        if not existing:
            raise
        group_id = existing["GroupId"]

    created = ec2.describe_security_groups(GroupIds=[group_id])["SecurityGroups"][0]
    if created.get("IpPermissions"):
        ec2.revoke_security_group_ingress(
            GroupId=group_id,
            IpPermissions=created["IpPermissions"],
        )
    if created.get("IpPermissionsEgress"):
        ec2.revoke_security_group_egress(
            GroupId=group_id,
            IpPermissions=created["IpPermissionsEgress"],
        )

    verified = ec2.describe_security_groups(GroupIds=[group_id])["SecurityGroups"][0]
    _validate_ruleless(verified)
    details["group_id"] = group_id
    log(
        "quarantine_security_group_ready",
        incident_id=incident_id,
        group_id=group_id,
        vpc_id=vpc_id,
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="ensure_quarantine_security_group",
        incident_id=incident_id,
        dry_run=False,
        status="completed",
        details=details,
    )
