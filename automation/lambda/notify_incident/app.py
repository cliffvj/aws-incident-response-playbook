from __future__ import annotations
import json, os, boto3
from aws_ir.context import region_from
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.validation import dry_run, require_incident, require_string


def handler(event, context):
    incident_id=require_incident(event); message=require_string(event,"message"); severity=require_string(event,"severity"); is_dry=dry_run(event); region=region_from(event)
    topic_arn=event.get("topic_arn") or os.environ.get("INCIDENT_TOPIC_ARN")
    if not topic_arn: raise ValueError("topic_arn or INCIDENT_TOPIC_ARN is required")
    payload={"incident_id":incident_id,"severity":severity,"message":message,"requested_by":event.get("requested_by"),"reason":event.get("reason")}
    details={"topic_arn":topic_arn,"payload":payload}
    if is_dry:
        return result(action="notify_incident",incident_id=incident_id,dry_run=True,status="planned",details=details)
    rsp=boto3.client("sns",region_name=region).publish(TopicArn=topic_arn,Subject=f"[{severity}] AWS incident {incident_id}"[:100],Message=json.dumps(payload,sort_keys=True))
    details["message_id"]=rsp.get("MessageId")
    log("incident_notification_published",incident_id=incident_id,severity=severity,message_id=details["message_id"],request_id=getattr(context,"aws_request_id",None))
    return result(action="notify_incident",incident_id=incident_id,dry_run=False,status="completed",details=details)
