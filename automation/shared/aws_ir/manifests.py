from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from .errors import ValidationError
from .validation import require_mapping, require_true

MANIFEST_VERSION = 1


def _canonical_bytes(value: dict[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")


def _checksum(value: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def create_manifest(
    *,
    action: str,
    incident_id: str,
    resource_type: str,
    resource_id: str,
    account_id: str,
    region: str,
    state: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "manifest_version": MANIFEST_VERSION,
        "action": action,
        "incident_id": incident_id,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "resource": {
            "type": resource_type,
            "id": resource_id,
            "account_id": account_id,
            "region": region,
        },
        "state": deepcopy(state),
    }
    if metadata:
        manifest["metadata"] = deepcopy(metadata)
    manifest["checksum_sha256"] = _checksum(manifest)
    return manifest


def validate_manifest(
    manifest: dict[str, Any],
    *,
    expected_action: str,
    expected_resource_type: str,
    expected_resource_id: str | None = None,
    expected_incident_id: str | None = None,
) -> dict[str, Any]:
    if manifest.get("manifest_version") != MANIFEST_VERSION:
        raise ValidationError(f"rollback_manifest.manifest_version must be {MANIFEST_VERSION}")
    if manifest.get("action") != expected_action:
        raise ValidationError(f"rollback_manifest.action must be {expected_action}")
    if expected_incident_id and manifest.get("incident_id") != expected_incident_id:
        raise ValidationError("rollback_manifest incident_id does not match the invocation")

    resource = manifest.get("resource")
    if not isinstance(resource, dict):
        raise ValidationError("rollback_manifest.resource must be an object")
    if resource.get("type") != expected_resource_type:
        raise ValidationError(
            f"rollback_manifest.resource.type must be {expected_resource_type}"
        )
    if expected_resource_id and resource.get("id") != expected_resource_id:
        raise ValidationError("rollback_manifest resource ID does not match the invocation")
    if not isinstance(manifest.get("state"), dict):
        raise ValidationError("rollback_manifest.state must be an object")

    supplied_checksum = manifest.get("checksum_sha256")
    if not isinstance(supplied_checksum, str):
        raise ValidationError("rollback_manifest.checksum_sha256 is required")
    unsigned = deepcopy(manifest)
    unsigned.pop("checksum_sha256", None)
    if _checksum(unsigned) != supplied_checksum:
        raise ValidationError("rollback_manifest checksum does not match its contents")
    return manifest


def rollback_manifest_from(
    event: dict[str, Any],
    *,
    expected_action: str,
    expected_resource_type: str,
    expected_resource_id: str | None = None,
    expected_incident_id: str | None = None,
) -> dict[str, Any]:
    manifest = require_mapping(event, "rollback_manifest")
    require_true(event, "confirm_restore")
    return validate_manifest(
        manifest,
        expected_action=expected_action,
        expected_resource_type=expected_resource_type,
        expected_resource_id=expected_resource_id,
        expected_incident_id=expected_incident_id,
    )
