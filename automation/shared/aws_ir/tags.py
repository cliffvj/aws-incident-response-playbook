from __future__ import annotations

from typing import Mapping


def _trim(value: str, limit: int = 256) -> str:
    return value[:limit]


def incident_tag_map(
    incident_id: str,
    requested_by: str | None = None,
    *,
    action: str | None = None,
    extra: Mapping[str, str] | None = None,
) -> dict[str, str]:
    tags = {
        "IncidentId": _trim(incident_id),
        "ManagedBy": "aws-ir-playbook",
    }
    if requested_by:
        tags["RequestedBy"] = _trim(requested_by)
    if action:
        tags["ResponseAction"] = _trim(action)
    if extra:
        for key, value in extra.items():
            tags[_trim(str(key), 128)] = _trim(str(value))
    return tags


def incident_tags(
    incident_id: str,
    requested_by: str | None = None,
    *,
    action: str | None = None,
    extra: Mapping[str, str] | None = None,
) -> list[dict[str, str]]:
    return [
        {"Key": key, "Value": value}
        for key, value in sorted(
            incident_tag_map(
                incident_id,
                requested_by,
                action=action,
                extra=extra,
            ).items()
        )
    ]
