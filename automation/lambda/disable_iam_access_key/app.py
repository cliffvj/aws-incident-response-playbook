from __future__ import annotations
import boto3
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.validation import dry_run, require_incident, require_string


def handler(event, context):
    incident_id=require_incident(event); username=require_string(event,"user_name"); key_id=require_string(event,"access_key_id"); is_dry=dry_run(event)
    iam=boto3.client("iam")
    last_used=iam.get_access_key_last_used(AccessKeyId=key_id).get("AccessKeyLastUsed",{})
    details={"user_name":username,"access_key_id_suffix":key_id[-4:],"last_used":last_used}
    if is_dry:
        return result(action="disable_iam_access_key",incident_id=incident_id,dry_run=True,status="planned",details=details)
    iam.update_access_key(UserName=username,AccessKeyId=key_id,Status="Inactive")
    log("iam_access_key_disabled",incident_id=incident_id,user_name=username,key_suffix=key_id[-4:],request_id=getattr(context,"aws_request_id",None))
    return result(action="disable_iam_access_key",incident_id=incident_id,dry_run=False,status="completed",details=details)
