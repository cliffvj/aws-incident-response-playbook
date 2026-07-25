from __future__ import annotations

import os
from typing import Any

from .errors import ValidationError
from .validation import optional_account_id, validate_region


def region_from(event: dict[str, Any]) -> str:
    region = (
        event.get("region")
        or os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    if not isinstance(region, str):
        raise ValidationError("region must be a string")
    return validate_region(region.strip())


def same_account_id(event: dict[str, Any], sts_client: Any) -> str:
    caller_account = sts_client.get_caller_identity()["Account"]
    expected_account = optional_account_id(event)
    if expected_account and expected_account != caller_account:
        raise ValidationError(
            f"expected_account_id {expected_account} does not match caller account {caller_account}"
        )
    return caller_account
