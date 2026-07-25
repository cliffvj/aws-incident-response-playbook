from __future__ import annotations

import boto3

from aws_ir.context import region_from, same_account_id
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.tags import incident_tags
from aws_ir.validation import dry_run, require_incident, require_instance_id


def _existing_snapshot(ec2, incident_id: str, volume_id: str) -> dict | None:
    response = ec2.describe_snapshots(
        OwnerIds=["self"],
        Filters=[
            {"Name": "tag:IncidentId", "Values": [incident_id]},
            {"Name": "tag:SourceVolumeId", "Values": [volume_id]},
            {"Name": "tag:ManagedBy", "Values": ["aws-ir-playbook"]},
        ],
    )
    candidates = [
        item
        for item in response.get("Snapshots", [])
        if item.get("State") not in {"error"}
    ]
    return sorted(candidates, key=lambda item: str(item.get("StartTime")), reverse=True)[0] if candidates else None


def handler(event, context):
    incident_id = require_incident(event)
    instance_id = require_instance_id(event)
    is_dry = dry_run(event)
    region = region_from(event)
    requested_by = event.get("requested_by")
    account_id = same_account_id(event, boto3.client("sts"))

    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances(InstanceIds=[instance_id])
    reservations = response.get("Reservations", [])
    if not reservations or not reservations[0].get("Instances"):
        raise ValueError(f"instance not found: {instance_id}")
    instance = reservations[0]["Instances"][0]
    volumes = [
        mapping["Ebs"]["VolumeId"]
        for mapping in instance.get("BlockDeviceMappings", [])
        if mapping.get("Ebs")
    ]
    if not volumes:
        raise ValueError("instance has no attached EBS volumes")

    existing = {
        volume_id: _existing_snapshot(ec2, incident_id, volume_id)
        for volume_id in volumes
    }
    pending = [volume_id for volume_id, snapshot in existing.items() if snapshot is None]
    details = {
        "account_id": account_id,
        "instance_id": instance_id,
        "region": region,
        "volume_ids": volumes,
        "existing_snapshots": [
            {
                "volume_id": volume_id,
                "snapshot_id": snapshot.get("SnapshotId"),
                "state": snapshot.get("State"),
            }
            for volume_id, snapshot in existing.items()
            if snapshot is not None
        ],
        "volumes_requiring_snapshot": pending,
        "snapshots": [],
    }

    if not pending:
        return result(
            action="snapshot_ebs_volumes",
            incident_id=incident_id,
            dry_run=is_dry,
            status="no_change",
            details=details,
        )
    if is_dry:
        return result(
            action="snapshot_ebs_volumes",
            incident_id=incident_id,
            dry_run=True,
            status="planned",
            details=details,
        )

    for volume_id in pending:
        snapshot = ec2.create_snapshot(
            VolumeId=volume_id,
            Description=f"Incident {incident_id} evidence snapshot for {instance_id}",
            TagSpecifications=[
                {
                    "ResourceType": "snapshot",
                    "Tags": incident_tags(
                        incident_id,
                        requested_by,
                        action="snapshot_ebs_volumes",
                        extra={
                            "SourceInstanceId": instance_id,
                            "SourceVolumeId": volume_id,
                        },
                    ),
                }
            ],
        )
        details["snapshots"].append(
            {"volume_id": volume_id, "snapshot_id": snapshot["SnapshotId"]}
        )
    log(
        "ebs_snapshots_created",
        incident_id=incident_id,
        instance_id=instance_id,
        snapshot_count=len(details["snapshots"]),
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="snapshot_ebs_volumes",
        incident_id=incident_id,
        dry_run=False,
        status="submitted",
        details=details,
    )
