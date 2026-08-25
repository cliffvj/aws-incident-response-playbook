#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

PLACEHOLDERS = {
    "partition": "aws",
    "collect_metadata_arn": "arn:aws:lambda:us-east-1:111122223333:function:collect",
    "snapshot_ebs_arn": "arn:aws:lambda:us-east-1:111122223333:function:snapshot",
    "ensure_quarantine_arn": "arn:aws:lambda:us-east-1:111122223333:function:quarantine",
    "isolate_ec2_arn": "arn:aws:lambda:us-east-1:111122223333:function:isolate",
    "restore_ec2_arn": "arn:aws:lambda:us-east-1:111122223333:function:restore",
    "notify_incident_arn": "arn:aws:lambda:us-east-1:111122223333:function:notify",
    "approval_topic_arn": "arn:aws:sns:us-east-1:111122223333:approval",
    "execution_table_name": "aws-ir-orchestration-executions",
    "approval_timeout_seconds": "3600",
}

REQUIRED_STATES = {
    "AcquireExecutionLock",
    "CollectTriageMetadata",
    "SnapshotEvidence",
    "RequestContainmentApproval",
    "IsolateInstanceLive",
    "PlanRollback",
    "RequestRollbackApproval",
    "ExecuteRollbackLive",
    "DuplicateExecution",
    "RecordWorkflowFailure",
}


def render_template(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in PLACEHOLDERS:
            raise ValueError(f"unknown template placeholder: {name}")
        return PLACEHOLDERS[name]

    rendered = re.sub(r"\$\{([A-Za-z0-9_]+)\}", replace, text)
    return rendered.replace('"__APPROVAL_TIMEOUT_SECONDS__"', PLACEHOLDERS["approval_timeout_seconds"])


def targets(state: dict[str, Any]) -> list[str]:
    result: list[str] = []
    if isinstance(state.get("Next"), str):
        result.append(state["Next"])
    if isinstance(state.get("Default"), str):
        result.append(state["Default"])
    for choice in state.get("Choices", []):
        if isinstance(choice.get("Next"), str):
            result.append(choice["Next"])
    for catcher in state.get("Catch", []):
        if isinstance(catcher.get("Next"), str):
            result.append(catcher["Next"])
    return result


def validate_definition(definition: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    states = definition.get("States")
    if not isinstance(states, dict) or not states:
        return ["States must be a non-empty object"]

    start = definition.get("StartAt")
    if start not in states:
        errors.append(f"StartAt target does not exist: {start}")

    missing_required = sorted(REQUIRED_STATES - set(states))
    if missing_required:
        errors.append("missing required states: " + ", ".join(missing_required))

    for name, state in states.items():
        if not isinstance(state, dict):
            errors.append(f"{name}: state must be an object")
            continue
        state_type = state.get("Type")
        if state_type not in {"Pass", "Task", "Choice", "Fail", "Succeed", "Wait", "Parallel", "Map"}:
            errors.append(f"{name}: unsupported or missing Type {state_type!r}")
        if state.get("End") is True and "Next" in state:
            errors.append(f"{name}: state cannot contain both End and Next")
        for target in targets(state):
            if target not in states:
                errors.append(f"{name}: transition target does not exist: {target}")

    for approval_name in ("RequestContainmentApproval", "RequestRollbackApproval"):
        state = states.get(approval_name, {})
        resource = str(state.get("Resource", ""))
        if not resource.endswith("sns:publish.waitForTaskToken"):
            errors.append(f"{approval_name}: must use SNS waitForTaskToken integration")
        serialized = json.dumps(state)
        if "$$.Task.Token" not in serialized:
            errors.append(f"{approval_name}: task token is not included in approval message")
        if not isinstance(state.get("TimeoutSeconds"), int) or state["TimeoutSeconds"] <= 0:
            errors.append(f"{approval_name}: TimeoutSeconds must be a positive integer")
        catches = state.get("Catch", [])
        if not any("States.Timeout" in c.get("ErrorEquals", []) for c in catches):
            errors.append(f"{approval_name}: must catch States.Timeout")

    acquire = states.get("AcquireExecutionLock", {})
    if "attribute_not_exists(event_id)" not in json.dumps(acquire):
        errors.append("AcquireExecutionLock: duplicate-event condition is missing")

    # Safety assertions: live containment and live rollback are separate states and
    # are reachable only from their approval-evaluation paths by construction.
    if states.get("EvaluateContainmentApproval", {}).get("Choices", [{}])[0].get("Next") != "EnsureQuarantineLive":
        errors.append("containment approval path does not lead to live quarantine preparation")
    if states.get("EvaluateRollbackApproval", {}).get("Choices", [{}])[0].get("Next") != "ExecuteRollbackLive":
        errors.append("rollback approval path does not lead to live restoration")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Render and structurally validate Step Functions ASL templates.")
    parser.add_argument(
        "path",
        nargs="?",
        default="automation/step-functions/ec2-incident-response.asl.json",
    )
    args = parser.parse_args()
    path = Path(args.path)
    raw = path.read_text(encoding="utf-8")
    try:
        rendered = render_template(raw)
        definition = json.loads(rendered)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {path}: {exc}")
        return 1

    errors = validate_definition(definition)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: validated Step Functions definition with {len(definition['States'])} states: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
