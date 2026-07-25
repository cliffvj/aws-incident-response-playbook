from __future__ import annotations

import boto3

from aws_ir.context import region_from, same_account_id
from aws_ir.errors import ValidationError
from aws_ir.logging import log
from aws_ir.manifests import create_manifest
from aws_ir.response import result
from aws_ir.s3_state import (
    BLOCK_ALL_PUBLIC_ACCESS,
    bucket_region,
    capture_bucket_public_access,
    public_access_block_matches,
)
from aws_ir.validation import dry_run, require_bucket_name, require_incident


def handler(event, context):
    incident_id = require_incident(event)
    bucket_name = require_bucket_name(event)
    is_dry = dry_run(event)
    region = region_from(event)
    account_id = same_account_id(event, boto3.client("sts"))
    s3 = boto3.client("s3", region_name=region)

    actual_region = bucket_region(s3, bucket_name, account_id)
    if actual_region != region:
        raise ValidationError(
            f"bucket is in {actual_region}; invoke again with region set to that value"
        )
    state = capture_bucket_public_access(
        s3,
        bucket_name=bucket_name,
        expected_owner=account_id,
    )
    manifest = create_manifest(
        action="contain_s3_public_access",
        incident_id=incident_id,
        resource_type="s3-bucket",
        resource_id=bucket_name,
        account_id=account_id,
        region=region,
        state=state,
        metadata={
            "containment": "bucket-level block public access",
            "policy_or_acl_modified": False,
        },
    )
    details = {
        "account_id": account_id,
        "bucket_name": bucket_name,
        "region": region,
        "observed_state": state,
        "target_public_access_block": BLOCK_ALL_PUBLIC_ACCESS,
        "rollback_manifest": manifest,
    }

    if public_access_block_matches(state, BLOCK_ALL_PUBLIC_ACCESS):
        return result(
            action="contain_s3_public_access",
            incident_id=incident_id,
            dry_run=is_dry,
            status="no_change",
            details=details,
        )
    if is_dry:
        return result(
            action="contain_s3_public_access",
            incident_id=incident_id,
            dry_run=True,
            status="planned",
            details=details,
        )

    s3.put_public_access_block(
        Bucket=bucket_name,
        ExpectedBucketOwner=account_id,
        PublicAccessBlockConfiguration=BLOCK_ALL_PUBLIC_ACCESS,
    )
    log(
        "s3_public_access_contained",
        incident_id=incident_id,
        bucket_name=bucket_name,
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="contain_s3_public_access",
        incident_id=incident_id,
        dry_run=False,
        status="completed",
        details=details,
    )
