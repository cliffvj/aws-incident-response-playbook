from __future__ import annotations

import json
import os

import boto3

from aws_ir.context import region_from, same_account_id
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.validation import dry_run, require_incident, require_string


def handler(event, context):
    incident_id = require_incident(event)
    message = require_string(event, "message")
    severity = require_string(event, "severity")
    is_dry = dry_run(event)
    region = region_from(event)
    account_id = same_account_id(event, boto3.client("sts"))
    topic_arn = event.get("topic_arn") or os.environ.get("INCIDENT_TOPIC_ARN")
    if not topic_arn:
        raise ValueError("topic_arn or INCIDENT_TOPIC_ARN is required")
    expected_prefix = f"arn:aws:sns:{region}:{account_id}:"
    if not topic_arn.startswith(expected_prefix):
        raise ValueError("SNS topic must be in the caller account and selected Region")

    payload = {
        "incident_id": incident_id,
        "severity": severity,
        "message": message,
        "requested_by": event.get("requested_by"),
        "reason": event.get("reason"),
    }
    details = {
        "account_id": account_id,
        "region": region,
        "topic_arn": topic_arn,
        "payload": payload,
    }
    if is_dry:
        return result(
            action="notify_incident",
            incident_id=incident_id,
            dry_run=True,
            status="planned",
            details=details,
        )

    response = boto3.client("sns", region_name=region).publish(
        TopicArn=topic_arn,
        Subject=f"[{severity}] AWS incident {incident_id}"[:100],
        Message=json.dumps(payload, sort_keys=True),
    )
    details["message_id"] = response.get("MessageId")
    log(
        "incident_notification_published",
        incident_id=incident_id,
        severity=severity,
        message_id=details["message_id"],
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="notify_incident",
        incident_id=incident_id,
        dry_run=False,
        status="completed",
        details=details,
    )
