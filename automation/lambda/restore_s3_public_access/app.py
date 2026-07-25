from __future__ import annotations

import boto3

from aws_ir.context import region_from, same_account_id
from aws_ir.errors import ValidationError
from aws_ir.logging import log
from aws_ir.manifests import rollback_manifest_from
from aws_ir.response import result
from aws_ir.s3_state import bucket_region, capture_bucket_public_access
from aws_ir.validation import dry_run, require_bucket_name, require_incident


def _target_public_access_block(manifest: dict) -> dict:
    value = manifest["state"].get("public_access_block")
    if not isinstance(value, dict) or "present" not in value:
        raise ValidationError("rollback manifest has no public access block state")
    configuration = value.get("configuration")
    if value["present"] and not isinstance(configuration, dict):
        raise ValidationError("rollback manifest public access block configuration is invalid")
    return value


def handler(event, context):
    incident_id = require_incident(event)
    bucket_name = require_bucket_name(event)
    is_dry = dry_run(event)
    region = region_from(event)
    account_id = same_account_id(event, boto3.client("sts"))
    manifest = rollback_manifest_from(
        event,
        expected_action="contain_s3_public_access",
        expected_resource_type="s3-bucket",
        expected_resource_id=bucket_name,
        expected_incident_id=incident_id,
    )
    resource = manifest["resource"]
    if resource.get("account_id") != account_id or resource.get("region") != region:
        raise ValidationError("rollback manifest account or Region does not match invocation")

    s3 = boto3.client("s3", region_name=region)
    actual_region = bucket_region(s3, bucket_name, account_id)
    if actual_region != region:
        raise ValidationError(
            f"bucket is in {actual_region}; invoke again with region set to that value"
        )
    current_state = capture_bucket_public_access(
        s3,
        bucket_name=bucket_name,
        expected_owner=account_id,
    )
    target = _target_public_access_block(manifest)
    current = current_state["public_access_block"]
    details = {
        "account_id": account_id,
        "bucket_name": bucket_name,
        "region": region,
        "current_public_access_block": current,
        "target_public_access_block": target,
        "source_manifest_checksum": manifest["checksum_sha256"],
        "policy_and_acl_restoration": "not performed; containment did not modify them",
    }

    if current == target:
        return result(
            action="restore_s3_public_access",
            incident_id=incident_id,
            dry_run=is_dry,
            status="no_change",
            details=details,
        )
    if is_dry:
        return result(
            action="restore_s3_public_access",
            incident_id=incident_id,
            dry_run=True,
            status="planned",
            details=details,
        )

    if target["present"]:
        s3.put_public_access_block(
            Bucket=bucket_name,
            ExpectedBucketOwner=account_id,
            PublicAccessBlockConfiguration=target["configuration"],
        )
    else:
        s3.delete_public_access_block(
            Bucket=bucket_name,
            ExpectedBucketOwner=account_id,
        )
    log(
        "s3_public_access_restored",
        incident_id=incident_id,
        bucket_name=bucket_name,
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="restore_s3_public_access",
        incident_id=incident_id,
        dry_run=False,
        status="completed",
        details=details,
    )
