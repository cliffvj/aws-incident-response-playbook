from __future__ import annotations

import boto3

from aws_ir.context import same_account_id
from aws_ir.logging import log
from aws_ir.manifests import create_manifest
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

    iam = boto3.client("iam")
    key = _find_key(iam, user_name, access_key_id)
    last_used_response = iam.get_access_key_last_used(AccessKeyId=access_key_id)
    last_used = last_used_response.get("AccessKeyLastUsed", {})
    original_status = key.get("Status")
    manifest = create_manifest(
        action="disable_iam_access_key",
        incident_id=incident_id,
        resource_type="iam-access-key",
        resource_id=access_key_id,
        account_id=account_id,
        region="global",
        state={"user_name": user_name, "status": original_status},
    )
    details = {
        "account_id": account_id,
        "user_name": user_name,
        "access_key_id_suffix": access_key_id[-4:],
        "current_status": original_status,
        "last_used": last_used,
        "rollback_manifest": manifest,
    }

    if original_status == "Inactive":
        return result(
            action="disable_iam_access_key",
            incident_id=incident_id,
            dry_run=is_dry,
            status="no_change",
            details=details,
        )
    if is_dry:
        return result(
            action="disable_iam_access_key",
            incident_id=incident_id,
            dry_run=True,
            status="planned",
            details=details,
        )

    iam.update_access_key(
        UserName=user_name,
        AccessKeyId=access_key_id,
        Status="Inactive",
    )
    log(
        "iam_access_key_disabled",
        incident_id=incident_id,
        user_name=user_name,
        key_suffix=access_key_id[-4:],
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="disable_iam_access_key",
        incident_id=incident_id,
        dry_run=False,
        status="completed",
        details=details,
    )
