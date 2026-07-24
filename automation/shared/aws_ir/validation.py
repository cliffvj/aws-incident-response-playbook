from __future__ import annotations
from typing import Any
from .errors import ValidationError


def require_string(event: dict[str, Any], name: str) -> str:
    value = event.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{name} must be a non-empty string")
    return value.strip()


def dry_run(event: dict[str, Any]) -> bool:
    value = event.get("dry_run", True)
    if not isinstance(value, bool):
        raise ValidationError("dry_run must be a boolean")
    return value


def require_incident(event: dict[str, Any]) -> str:
    return require_string(event, "incident_id")
