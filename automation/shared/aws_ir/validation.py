from __future__ import annotations

import re
from typing import Any

from .errors import ValidationError

_ACCOUNT_ID = re.compile(r"^\d{12}$")
_BUCKET_NAME = re.compile(r"^(?!xn--)(?!sthree-)(?!amzn-s3-demo-)(?!.*\.\.)(?!.*\.-)(?!.*-\.)(?!\d{1,3}(?:\.\d{1,3}){3}$)[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$")
_INSTANCE_ID = re.compile(r"^i-[0-9a-f]{8,17}$")
_SECURITY_GROUP_ID = re.compile(r"^sg-[0-9a-f]{8,17}$")
_NETWORK_INTERFACE_ID = re.compile(r"^eni-[0-9a-f]{8,17}$")
_VPC_ID = re.compile(r"^vpc-[0-9a-f]{8,17}$")
_REGION = re.compile(r"^[a-z]{2}(?:-gov)?-[a-z]+-\d$")
_INCIDENT_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")


def require_string(event: dict[str, Any], name: str) -> str:
    value = event.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{name} must be a non-empty string")
    return value.strip()


def optional_string(event: dict[str, Any], name: str) -> str | None:
    value = event.get(name)
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{name} must be a non-empty string when supplied")
    return value.strip()


def require_mapping(event: dict[str, Any], name: str) -> dict[str, Any]:
    value = event.get(name)
    if not isinstance(value, dict):
        raise ValidationError(f"{name} must be an object")
    return value


def require_true(event: dict[str, Any], name: str) -> bool:
    value = event.get(name)
    if value is not True:
        raise ValidationError(f"{name} must be exactly true")
    return True


def dry_run(event: dict[str, Any]) -> bool:
    value = event.get("dry_run", True)
    if not isinstance(value, bool):
        raise ValidationError("dry_run must be a boolean")
    return value


def require_incident(event: dict[str, Any]) -> str:
    value = require_string(event, "incident_id")
    if not _INCIDENT_ID.fullmatch(value):
        raise ValidationError("incident_id contains unsupported characters or is too long")
    return value


def _validated_identifier(event: dict[str, Any], name: str, pattern: re.Pattern[str], label: str) -> str:
    value = require_string(event, name)
    if not pattern.fullmatch(value):
        raise ValidationError(f"{name} must be a valid {label}")
    return value


def require_account_id(event: dict[str, Any], name: str = "expected_account_id") -> str:
    return _validated_identifier(event, name, _ACCOUNT_ID, "12-digit AWS account ID")


def optional_account_id(event: dict[str, Any], name: str = "expected_account_id") -> str | None:
    value = optional_string(event, name)
    if value is not None and not _ACCOUNT_ID.fullmatch(value):
        raise ValidationError(f"{name} must be a valid 12-digit AWS account ID")
    return value


def require_bucket_name(event: dict[str, Any], name: str = "bucket_name") -> str:
    return _validated_identifier(event, name, _BUCKET_NAME, "general purpose S3 bucket name")


def require_instance_id(event: dict[str, Any], name: str = "instance_id") -> str:
    return _validated_identifier(event, name, _INSTANCE_ID, "EC2 instance ID")


def require_security_group_id(event: dict[str, Any], name: str = "quarantine_security_group_id") -> str:
    return _validated_identifier(event, name, _SECURITY_GROUP_ID, "security group ID")


def require_network_interface_id(event: dict[str, Any], name: str = "network_interface_id") -> str:
    return _validated_identifier(event, name, _NETWORK_INTERFACE_ID, "network interface ID")


def require_vpc_id(event: dict[str, Any], name: str = "vpc_id") -> str:
    return _validated_identifier(event, name, _VPC_ID, "VPC ID")


def validate_region(value: str) -> str:
    if not _REGION.fullmatch(value):
        raise ValidationError("region must look like a valid AWS Region identifier")
    return value
