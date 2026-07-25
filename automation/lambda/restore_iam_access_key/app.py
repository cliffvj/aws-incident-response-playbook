from __future__ import annotations

import boto3

from aws_ir.context import same_account_id
from aws_ir.errors import ValidationError
from aws_ir.logging import log
from aws_ir.manifests import rollback_manifest_from
from aws_ir.response import result
from aws_ir.validation import dry_run, require_incident, require_string


def _find_key(iam, user_name: str, access_key_id: str) -> dict:
    response = iam.list_access_keys(UserName=user_name)
    for item in response.get("AccessKeyMetadata", []):
        if item.get("AccessKeyId") == access_key_id:
            return item
    raise ValueError("access key does not belong to the supplied IAM user")


def handler(event, context):
    incident_id = require_incident(event)
    user_name = require_string(event, "user_name")
    access_key_id = require_string(event, "access_key_id")
    is_dry = dry_run(event)
    account_id = same_account_id(event, boto3.client("sts"))
    manifest = rollback_manifest_from(
        event,
        expected_action="disable_iam_access_key",
        expected_resource_type="iam-access-key",
        expected_resource_id=access_key_id,
        expected_incident_id=incident_id,
    )
    if manifest["resource"].get("account_id") != account_id:
        raise ValidationError("rollback manifest account does not match invocation")
    state = manifest["state"]
    if state.get("user_name") != user_name:
        raise ValidationError("rollback manifest IAM user does not match invocation")
    target_status = state.get("status")
    if target_status not in {"Active", "Inactive"}:
        raise ValidationError("rollback manifest access key status is invalid")

    iam = boto3.client("iam")
    key = _find_key(iam, user_name, access_key_id)
    current_status = key.get("Status")
    details = {
        "account_id": account_id,
        "user_name": user_name,
        "access_key_id_suffix": access_key_id[-4:],
        "current_status": current_status,
        "target_status": target_status,
        "source_manifest_checksum": manifest["checksum_sha256"],
    }

    if current_status == target_status:
        return result(
            action="restore_iam_access_key",
            incident_id=incident_id,
            dry_run=is_dry,
            status="no_change",
            details=details,
        )
    if is_dry:
        return result(
            action="restore_iam_access_key",
            incident_id=incident_id,
            dry_run=True,
            status="planned",
            details=details,
        )

    iam.update_access_key(
        UserName=user_name,
        AccessKeyId=access_key_id,
        Status=target_status,
    )
    log(
        "iam_access_key_restored",
        incident_id=incident_id,
        user_name=user_name,
        key_suffix=access_key_id[-4:],
        target_status=target_status,
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="restore_iam_access_key",
        incident_id=incident_id,
        dry_run=False,
        status="completed",
        details=details,
    )
