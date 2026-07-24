from __future__ import annotations
import boto3
from aws_ir.context import region_from
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.validation import require_incident, require_string


def handler(event, context):
    incident_id=require_incident(event); instance_id=require_string(event,"instance_id"); region=region_from(event)
    ec2=boto3.client("ec2",region_name=region)
    response=ec2.describe_instances(InstanceIds=[instance_id])
    reservations=response.get("Reservations",[])
    if not reservations or not reservations[0].get("Instances"):
        raise ValueError(f"instance not found: {instance_id}")
    i=reservations[0]["Instances"][0]
    details={
      "instance_id":instance_id,"region":region,"state":i.get("State",{}).get("Name"),"vpc_id":i.get("VpcId"),"subnet_id":i.get("SubnetId"),
      "security_groups":i.get("SecurityGroups",[]),"network_interfaces":[{"id":n.get("NetworkInterfaceId"),"private_ip":n.get("PrivateIpAddress"),"groups":n.get("Groups",[])} for n in i.get("NetworkInterfaces",[])],
      "volumes":[b.get("Ebs",{}).get("VolumeId") for b in i.get("BlockDeviceMappings",[]) if b.get("Ebs")],
      "iam_instance_profile":i.get("IamInstanceProfile"),"tags":i.get("Tags",[]),"launch_time":i.get("LaunchTime")
    }
    log("ec2_metadata_collected",incident_id=incident_id,instance_id=instance_id,request_id=getattr(context,"aws_request_id",None))
    return result(action="collect_ec2_metadata",incident_id=incident_id,dry_run=True,status="observed",details=details)
