from __future__ import annotations

import boto3

from aws_ir.context import region_from, same_account_id
from aws_ir.errors import ValidationError
from aws_ir.logging import log
from aws_ir.response import result
from aws_ir.s3_state import bucket_region, capture_bucket_public_access
from aws_ir.validation import require_bucket_name, require_incident


def handler(event, context):
    incident_id = require_incident(event)
    bucket_name = require_bucket_name(event)
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
    details = {
        "account_id": account_id,
        "bucket_name": bucket_name,
        "region": actual_region,
        "state": state,
    }
    log(
        "s3_public_access_inspected",
        incident_id=incident_id,
        bucket_name=bucket_name,
        region=actual_region,
        request_id=getattr(context, "aws_request_id", None),
    )
    return result(
        action="inspect_s3_public_access",
        incident_id=incident_id,
        dry_run=True,
        status="observed",
        details=details,
    )
