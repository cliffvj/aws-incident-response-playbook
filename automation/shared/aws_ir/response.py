from __future__ import annotations
from typing import Any


def result(*, action: str, incident_id: str, dry_run: bool, status: str, details: dict[str, Any]) -> dict[str, Any]:
    return {"action": action, "incident_id": incident_id, "dry_run": dry_run, "status": status, "details": details}
