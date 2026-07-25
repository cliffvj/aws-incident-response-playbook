from __future__ import annotations

import boto3

from aws_ir.context import region_from, same_account_id
from aws_ir.errors import ValidationError
from aws_ir.logging import log
from aws_ir.manifests import rollback_manifest_from
from aws_ir.response import result
from aws_ir.validation import dry_run, require_incident, require_instance_id


def handler(event, context):
    incident_id = require_incident(event)
    instance_id = require_instance_id(event)
    is_dry = dry_run(event)
    region = region_from(event)
    account_id = same_account_id(event, boto3.client("sts"))
    manifest = rollback_manifest_from(
        event,
        expected_action="isolate_ec2_instance",
        expected_resource_type="ec2-instance",
        expected_resource_id=instance_id,
        expected_incident_id=incident_id,
    )
    resource = manifest["resource"]
    if resource.get("account_id") != account_id or resource.get("region") != region:
        raise ValidationError("rollback manifest account or Region does not match invocation")

    requested_state = manifest["state"].get("network_interfaces")
    if not isinstance(requested_state, list) or not requested_state:
        raise ValidationError("rollback manifest contains no network interface state")

    ec2 = boto3.client("ec2", region_name=region)
    interface_ids = [item.get("network_interface_id") for item in requested_state]
    response = ec2.describe_network_interfaces(NetworkInterfaceIds=interface_ids)
    current_by_id = {
        item["NetworkInterfaceId"]: [group["GroupId"] for group in item.get("Groups", [])]
        for item in response.get("NetworkInterfaces", [])
    }

    changes = []
    for item in requested_state:
        interface_id = item.get("network_interface_id")
        target_groups = item.get("security_group_ids")
        if not isinstance(interface_id, str) or not isinstance(target_groups, list) or not target_groups:
            raise ValidationError("rollback manifest network interface state is invalid")
        if interface_id not in current_by_id:
            raise ValidationError(f"network interface not found: {interface_id}")
        if current_by_id[interface_id] != target_groups:
            changes.append(
                {
                    "network_interface_id": interface_id,
                    "current_security_group_ids": current_by_id[interface_id],
                    "target_security_group_ids": target_groups,
                }
            )

    details = {
        "account_id": account_id,
        "instance_id": instance_id,
        "region": region,
        "changes": changes,
        "source_manifest_checksum": manifest["checksum_sha256"],
    }
    if not changes:
        return result(
            action="restore_ec2_security_groups",
            incident_id=incident_id,
            dry_run=is_dry,
            status="no_change",
            details=details,
        )
    if is_dry:
        return result(
            action="restore_ec2_security_groups",
            incident_id=incident_id,
            dry_run=True,
            status="planned",
            details=details,
        )

    for change in changes:
        ec2.modify_network_interface_attribute(
            NetworkInterfaceId=change["network_interface_id"],
            Groups=change["target_security_group_ids"],
        )
    log(
        "ec2_security_groups_restored",
        incident_id=incident_id,
        instance_id=instance_id,
        network_interface_ids=[item["network_interface_id"] for item in changes],
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="restore_ec2_security_groups",
        incident_id=incident_id,
        dry_run=False,
        status="completed",
        details=details,
    )
