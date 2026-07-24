from __future__ import annotations

def incident_tags(incident_id: str, requested_by: str | None = None) -> list[dict[str, str]]:
    tags = [{"Key": "IncidentId", "Value": incident_id}, {"Key": "ManagedBy", "Value": "aws-ir-playbook"}]
    if requested_by:
        tags.append({"Key": "RequestedBy", "Value": requested_by[:256]})
    return tags
