from __future__ import annotations
import boto3
from aws_ir.context import region_from
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.tags import incident_tags
from aws_ir.validation import dry_run, require_incident, require_string


def handler(event, context):
    incident_id=require_incident(event); instance_id=require_string(event,"instance_id"); is_dry=dry_run(event); region=region_from(event); requested_by=event.get("requested_by")
    ec2=boto3.client("ec2",region_name=region)
    r=ec2.describe_instances(InstanceIds=[instance_id]); i=r["Reservations"][0]["Instances"][0]
    volumes=[b["Ebs"]["VolumeId"] for b in i.get("BlockDeviceMappings",[]) if b.get("Ebs")]
    details={"instance_id":instance_id,"volume_ids":volumes,"snapshots":[]}
    if is_dry:
        return result(action="snapshot_ebs_volumes",incident_id=incident_id,dry_run=True,status="planned",details=details)
    for volume_id in volumes:
        rsp=ec2.create_snapshot(VolumeId=volume_id,Description=f"Incident {incident_id} evidence snapshot for {instance_id}",TagSpecifications=[{"ResourceType":"snapshot","Tags":incident_tags(incident_id,requested_by)}])
        details["snapshots"].append({"volume_id":volume_id,"snapshot_id":rsp["SnapshotId"]})
    log("ebs_snapshots_created",incident_id=incident_id,instance_id=instance_id,snapshot_count=len(details["snapshots"]),request_id=getattr(context,"aws_request_id",None))
    return result(action="snapshot_ebs_volumes",incident_id=incident_id,dry_run=False,status="submitted",details=details)
