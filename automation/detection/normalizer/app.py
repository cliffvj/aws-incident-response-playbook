from __future__ import annotations

import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from typing import Any

import boto3
from botocore.exceptions import ClientError

_INSTANCE_ID = re.compile(r"^i-[0-9a-f]{8,17}$")
_ACCOUNT_ID = re.compile(r"^\d{12}$")
_ALLOWED_ROUTES = {"notify_only", "triage"}


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"missing required environment variable: {name}")
    return value


def _json_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _severity_guardduty(detail: dict[str, Any]) -> str:
    try:
        value = float(detail.get("severity", 0))
    except (TypeError, ValueError):
        value = 0.0
    if value >= 7.0:
        return "HIGH"
    if value >= 4.0:
        return "MEDIUM"
    return "LOW"


def _severity_securityhub(finding: dict[str, Any]) -> str:
    label = finding.get("Severity", {}).get("Label")
    if isinstance(label, str):
        label = label.upper()
        if label in {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFORMATIONAL"}:
            return label
    normalized = finding.get("Severity", {}).get("Normalized")
    if isinstance(normalized, (int, float)):
        if normalized >= 70:
            return "HIGH"
        if normalized >= 40:
            return "MEDIUM"
    return "LOW"


def _ec2_from_securityhub(finding: dict[str, Any]) -> str | None:
    for resource in finding.get("Resources", []) or []:
        if resource.get("Type") != "AwsEc2Instance":
            continue
        resource_id = str(resource.get("Id", ""))
        candidate = resource_id.rsplit("/", 1)[-1]
        if _INSTANCE_ID.fullmatch(candidate):
            return candidate
    return None


def _principal_arn(event: dict[str, Any]) -> str:
    identity = event.get("detail", {}).get("userIdentity", {})
    if not isinstance(identity, dict):
        return ""
    arn = identity.get("arn")
    if isinstance(arn, str):
        return arn
    issuer = identity.get("sessionContext", {}).get("sessionIssuer", {})
    return issuer.get("arn", "") if isinstance(issuer, dict) else ""


def _ignored_principal(event: dict[str, Any]) -> bool:
    prefixes = [item.strip() for item in os.environ.get("IGNORE_PRINCIPAL_ARN_PREFIXES", "").split(",") if item.strip()]
    principal = _principal_arn(event)
    return bool(principal and any(principal.startswith(prefix) for prefix in prefixes))


def _normalize(event: dict[str, Any]) -> dict[str, Any]:
    source = str(event.get("source", ""))
    detail_type = str(event.get("detail-type", ""))
    detail = event.get("detail") if isinstance(event.get("detail"), dict) else {}
    account_id = str(event.get("account", ""))
    region = str(event.get("region", ""))
    observed_at = str(event.get("time") or datetime.now(timezone.utc).isoformat())
    provider_id = str(event.get("id", ""))

    severity = "LOW"
    title = detail_type or source or "AWS security event"
    finding_id = provider_id
    resource_type = "unknown"
    resource_id = None

    if source == "aws.guardduty" and detail_type == "GuardDuty Finding":
        severity = _severity_guardduty(detail)
        finding_id = str(detail.get("id") or provider_id)
        title = str(detail.get("title") or detail.get("type") or "GuardDuty finding")
        instance_id = detail.get("resource", {}).get("instanceDetails", {}).get("instanceId")
        if isinstance(instance_id, str) and _INSTANCE_ID.fullmatch(instance_id):
            resource_type, resource_id = "ec2_instance", instance_id

    elif source == "aws.securityhub" and detail_type == "Security Hub Findings - Imported":
        findings = detail.get("findings") or []
        finding = findings[0] if findings and isinstance(findings[0], dict) else {}
        severity = _severity_securityhub(finding)
        finding_id = str(finding.get("Id") or provider_id)
        title = str(finding.get("Title") or "Security Hub finding")
        instance_id = _ec2_from_securityhub(finding)
        if instance_id:
            resource_type, resource_id = "ec2_instance", instance_id

    elif source == "aws.config" and detail_type == "Config Rules Compliance Change":
        compliance = detail.get("newEvaluationResult", {}).get("complianceType")
        severity = "MEDIUM" if compliance == "NON_COMPLIANT" else "LOW"
        resource_type_raw = detail.get("resourceType") or detail.get("newEvaluationResult", {}).get("evaluationResultIdentifier", {}).get("evaluationResultQualifier", {}).get("resourceType")
        resource_id_raw = detail.get("resourceId") or detail.get("newEvaluationResult", {}).get("evaluationResultIdentifier", {}).get("evaluationResultQualifier", {}).get("resourceId")
        title = f"AWS Config compliance change: {compliance or 'UNKNOWN'}"
        if resource_type_raw == "AWS::EC2::Instance" and isinstance(resource_id_raw, str) and _INSTANCE_ID.fullmatch(resource_id_raw):
            resource_type, resource_id = "ec2_instance", resource_id_raw
        elif isinstance(resource_id_raw, str):
            resource_type, resource_id = str(resource_type_raw or "config_resource"), resource_id_raw
        finding_id = str(detail.get("configRuleName") or provider_id)

    elif source == "aws.cloudwatch" and detail_type == "CloudWatch Alarm State Change":
        state_value = detail.get("state", {}).get("value")
        severity = "MEDIUM" if state_value == "ALARM" else "LOW"
        title = f"CloudWatch alarm {detail.get('alarmName', 'unknown')} entered {state_value or 'UNKNOWN'}"
        resources = event.get("resources") or []
        if resources:
            resource_type, resource_id = "cloudwatch_alarm", str(resources[0])
        finding_id = str(detail.get("alarmName") or provider_id)

    elif detail_type == "AWS API Call via CloudTrail":
        event_source = detail.get("eventSource")
        event_name = detail.get("eventName")
        high_risk = {"StopLogging", "DeleteTrail", "UpdateTrail", "PutEventSelectors", "DeleteEventDataStore"}
        severity = "HIGH" if event_name in high_risk else "MEDIUM"
        title = f"CloudTrail API event: {event_source or 'unknown'} {event_name or 'unknown'}"
        finding_id = str(detail.get("eventID") or provider_id)

    elif source == "aws-ir.lab" and detail_type == "Simulated Security Finding":
        severity = str(detail.get("severity", "MEDIUM")).upper()
        title = str(detail.get("title") or "Authorized AWS IR lab finding")
        finding_id = str(detail.get("finding_id") or provider_id)
        instance_id = detail.get("instance_id")
        if isinstance(instance_id, str) and _INSTANCE_ID.fullmatch(instance_id):
            resource_type, resource_id = "ec2_instance", instance_id

    else:
        raise ValueError(f"unsupported event source/detail-type: {source}/{detail_type}")

    if account_id and not _ACCOUNT_ID.fullmatch(account_id):
        raise ValueError("event account must be a 12-digit AWS account ID")

    dedupe_seed = {
        "source": source,
        "detail_type": detail_type,
        "finding_id": finding_id,
        "resource_id": resource_id,
    }
    dedupe_key = _json_hash(dedupe_seed)
    incident_id = f"EVT-{dedupe_key[:20]}"

    return {
        "schema": "aws-ir-normalized-security-event/v1",
        "event_id": provider_id or dedupe_key[:32],
        "dedupe_key": dedupe_key,
        "incident_id": incident_id,
        "source": source,
        "detail_type": detail_type,
        "source_account_id": account_id,
        "source_region": region,
        "observed_at": observed_at,
        "severity": severity,
        "title": title[:512],
        "finding_id": finding_id[:512],
        "resource_type": resource_type,
        "resource_id": resource_id,
        "raw_event_sha256": _json_hash(event),
    }


def _allowed_account(account_id: str) -> bool:
    allowed = [item.strip() for item in os.environ.get("ALLOWED_ACCOUNT_IDS", "").split(",") if item.strip()]
    return not allowed or account_id in allowed


def _acquire_dedupe(item: dict[str, Any]) -> bool:
    table_name = _require_env("DEDUP_TABLE_NAME")
    ttl_seconds = int(os.environ.get("DEDUP_TTL_SECONDS", "86400"))
    expires_at = int(time.time()) + max(60, ttl_seconds)
    dynamodb = boto3.client("dynamodb", region_name=item.get("source_region") or None)
    try:
        dynamodb.put_item(
            TableName=table_name,
            Item={
                "dedupe_key": {"S": item["dedupe_key"]},
                "incident_id": {"S": item["incident_id"]},
                "source": {"S": item["source"]},
                "expires_at": {"N": str(expires_at)},
            },
            ConditionExpression="attribute_not_exists(dedupe_key)",
        )
        return True
    except ClientError as error:
        code = str(error.response.get("Error", {}).get("Code", ""))
        if code == "ConditionalCheckFailedException":
            return False
        raise


def _route(item: dict[str, Any]) -> str:
    route = os.environ.get("DEFAULT_RESPONSE_ROUTE", "notify_only").strip().lower()
    if route not in _ALLOWED_ROUTES:
        route = "notify_only"
    if route == "triage" and item.get("resource_type") != "ec2_instance":
        return "notify_only"
    return route


def _notify(item: dict[str, Any], route: str) -> dict[str, Any]:
    topic_arn = _require_env("INCIDENT_TOPIC_ARN")
    sns = boto3.client("sns", region_name=item.get("source_region") or None)
    body = {
        "schema": item["schema"],
        "incident_id": item["incident_id"],
        "severity": item["severity"],
        "title": item["title"],
        "source": item["source"],
        "detail_type": item["detail_type"],
        "resource_type": item["resource_type"],
        "resource_id": item["resource_id"],
        "route": route,
        "raw_event_sha256": item["raw_event_sha256"],
    }
    response = sns.publish(
        TopicArn=topic_arn,
        Subject=f"AWS IR {item['severity']}: {item['incident_id']}"[:100],
        Message=json.dumps(body, sort_keys=True),
    )
    return {"route": "notify_only", "message_id": response.get("MessageId")}


def _start_triage(item: dict[str, Any]) -> dict[str, Any]:
    state_machine_arn = _require_env("STATE_MACHINE_ARN")
    states = boto3.client("stepfunctions", region_name=item.get("source_region") or None)
    payload = {
        "event_id": item["dedupe_key"][:64],
        "incident_id": item["incident_id"],
        "mode": "triage",
        "expected_account_id": item["source_account_id"],
        "region": item["source_region"],
        "instance_id": item["resource_id"],
        "requested_by": "eventbridge-detection-router",
        "reason": item["title"],
        "severity": item["severity"],
        "dry_run": True,
    }
    name = f"evt-{item['dedupe_key'][:48]}"
    response = states.start_execution(
        stateMachineArn=state_machine_arn,
        name=name,
        input=json.dumps(payload, separators=(",", ":")),
    )
    return {"route": "triage", "execution_arn": response.get("executionArn")}


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise ValueError("EventBridge payload must be a JSON object")
    if _ignored_principal(event):
        return {"status": "suppressed", "reason": "ignored_principal"}

    item = _normalize(event)
    if not _allowed_account(item["source_account_id"]):
        return {"status": "suppressed", "reason": "account_not_allowed", "normalized": item}

    if not _acquire_dedupe(item):
        return {"status": "duplicate", "normalized": item}

    route = _route(item)
    if route == "triage":
        routed = _start_triage(item)
    else:
        routed = _notify(item, route)

    return {
        "status": "routed",
        "route": routed["route"],
        "normalized": item,
        "target": routed,
        "request_id": getattr(context, "aws_request_id", None),
    }
