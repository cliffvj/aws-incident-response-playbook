from __future__ import annotations

import json
from typing import Any, Callable

from botocore.exceptions import ClientError

BLOCK_ALL_PUBLIC_ACCESS = {
    "BlockPublicAcls": True,
    "IgnorePublicAcls": True,
    "BlockPublicPolicy": True,
    "RestrictPublicBuckets": True,
}


def _error_code(error: ClientError) -> str:
    return str(error.response.get("Error", {}).get("Code", ""))


def _optional_call(
    call: Callable[..., dict[str, Any]],
    *,
    absent_codes: set[str],
    **kwargs: Any,
) -> dict[str, Any] | None:
    try:
        return call(**kwargs)
    except ClientError as error:
        if _error_code(error) in absent_codes:
            return None
        raise


def bucket_region(s3_client: Any, bucket_name: str, expected_owner: str) -> str:
    response = s3_client.get_bucket_location(
        Bucket=bucket_name,
        ExpectedBucketOwner=expected_owner,
    )
    location = response.get("LocationConstraint")
    if location is None:
        return "us-east-1"
    if location == "EU":
        return "eu-west-1"
    return str(location)


def capture_bucket_public_access(
    s3_client: Any,
    *,
    bucket_name: str,
    expected_owner: str,
) -> dict[str, Any]:
    kwargs = {"Bucket": bucket_name, "ExpectedBucketOwner": expected_owner}

    public_access_block_response = _optional_call(
        s3_client.get_public_access_block,
        absent_codes={"NoSuchPublicAccessBlockConfiguration"},
        **kwargs,
    )
    policy_response = _optional_call(
        s3_client.get_bucket_policy,
        absent_codes={"NoSuchBucketPolicy"},
        **kwargs,
    )
    ownership_response = _optional_call(
        s3_client.get_bucket_ownership_controls,
        absent_codes={"OwnershipControlsNotFoundError", "NoSuchOwnershipControls"},
        **kwargs,
    )

    policy_document = None
    if policy_response is not None:
        policy_document = json.loads(policy_response["Policy"])

    return {
        "public_access_block": {
            "present": public_access_block_response is not None,
            "configuration": (
                public_access_block_response.get("PublicAccessBlockConfiguration")
                if public_access_block_response
                else None
            ),
        },
        "policy": {
            "present": policy_response is not None,
            "document": policy_document,
        },
        "policy_status": s3_client.get_bucket_policy_status(**kwargs).get(
            "PolicyStatus", {"IsPublic": False}
        ),
        "acl": {
            key: value
            for key, value in s3_client.get_bucket_acl(**kwargs).items()
            if key in {"Owner", "Grants"}
        },
        "ownership_controls": (
            ownership_response.get("OwnershipControls") if ownership_response else None
        ),
    }


def public_access_block_matches(state: dict[str, Any], target: dict[str, bool]) -> bool:
    pab = state.get("public_access_block", {})
    return bool(pab.get("present")) and pab.get("configuration") == target
