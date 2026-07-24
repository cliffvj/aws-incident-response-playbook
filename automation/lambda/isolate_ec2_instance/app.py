from __future__ import annotations
import boto3
from aws_ir.context import region_from
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.validation import dry_run, require_incident, require_string


def handler(event, context):
    incident_id=require_incident(event); instance_id=require_string(event,"instance_id"); quarantine_sg=require_string(event,"quarantine_security_group_id"); is_dry=dry_run(event); region=region_from(event)
    ec2=boto3.client("ec2",region_name=region)
    r=ec2.describe_instances(InstanceIds=[instance_id]); i=r["Reservations"][0]["Instances"][0]
    original=[g["GroupId"] for g in i.get("SecurityGroups",[])]; vpc=i.get("VpcId")
    sg=ec2.describe_security_groups(GroupIds=[quarantine_sg])["SecurityGroups"][0]
    if sg.get("VpcId") != vpc: raise ValueError("quarantine security group must be in the instance VPC")
    details={"instance_id":instance_id,"vpc_id":vpc,"original_security_group_ids":original,"quarantine_security_group_id":quarantine_sg}
    if is_dry:
        log("ec2_isolation_planned",incident_id=incident_id,**details)
        return result(action="isolate_ec2_instance",incident_id=incident_id,dry_run=True,status="planned",details=details)
    ec2.modify_instance_attribute(InstanceId=instance_id,Groups=[quarantine_sg])
    log("ec2_isolated",incident_id=incident_id,request_id=getattr(context,"aws_request_id",None),**details)
    return result(action="isolate_ec2_instance",incident_id=incident_id,dry_run=False,status="completed",details=details)
