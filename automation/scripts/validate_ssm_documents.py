#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

DOC_DIR = Path("automation/ssm")
DOCUMENTS = {
    "collect-linux-evidence.json": ("Linux", "AWS-RunShellScript", "CollectLinuxEvidence"),
    "collect-windows-evidence.json": ("Windows", "AWS-RunPowerShellScript", "CollectWindowsEvidence"),
}
REQUIRED_PARAMETERS = {
    "AutomationAssumeRole",
    "InstanceId",
    "IncidentId",
    "EvidenceBucket",
    "EvidencePrefix",
}
FORBIDDEN_TOKENS = {
    "terminate-instances",
    "stop-instances",
    "reboot-instances",
    "rm -rf",
    "shutdown /s",
    "restart-computer",
    "stop-service",
    "remove-item",
    "disable-localuser",
}


def validate(path: Path, platform: str, command_document: str, collect_step: str) -> list[str]:
    errors: list[str] = []
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]

    if doc.get("schemaVersion") != "0.3":
        errors.append("schemaVersion must be 0.3 for Automation")
    if doc.get("assumeRole") != "{{AutomationAssumeRole}}":
        errors.append("runbook must use the AutomationAssumeRole parameter")
    params = set(doc.get("parameters", {}))
    if not REQUIRED_PARAMETERS.issubset(params):
        errors.append("missing parameters: " + ", ".join(sorted(REQUIRED_PARAMETERS - params)))

    steps = {step.get("name"): step for step in doc.get("mainSteps", [])}
    for required in ("PreflightManagedNode", collect_step, "FinalizeIntegrityManifest"):
        if required not in steps:
            errors.append(f"missing required step: {required}")

    preflight = steps.get("PreflightManagedNode", {})
    if preflight.get("action") != "aws:executeScript":
        errors.append("preflight must use aws:executeScript")
    preflight_blob = json.dumps(preflight).lower()
    for required in ("describe_instance_information", "ping_status", platform.lower()):
        if required not in preflight_blob:
            errors.append(f"preflight is missing {required!r} check")

    collect = steps.get(collect_step, {})
    if collect.get("action") != "aws:runCommand":
        errors.append("collection step must use aws:runCommand")
    inputs = collect.get("inputs", {})
    if inputs.get("DocumentName") != command_document:
        errors.append(f"collection must use {command_document}")
    if "OutputS3BucketName" not in inputs or "OutputS3KeyPrefix" not in inputs:
        errors.append("collection must send command output to S3")

    finalizer = steps.get("FinalizeIntegrityManifest", {})
    final_blob = json.dumps(finalizer).lower()
    if finalizer.get("action") != "aws:executeScript":
        errors.append("integrity finalizer must use aws:executeScript")
    for required in ("sha256", "integrity-manifest.json", "put_object", "get_object"):
        if required not in final_blob:
            errors.append(f"integrity finalizer is missing {required!r}")

    full_blob = path.read_text(encoding="utf-8").lower()
    for token in sorted(FORBIDDEN_TOKENS):
        if token in full_blob:
            errors.append(f"forbidden mutating token present: {token}")
    return errors


def main() -> int:
    failures = 0
    for filename, settings in DOCUMENTS.items():
        path = DOC_DIR / filename
        if not path.exists():
            print(f"ERROR: missing {path}")
            failures += 1
            continue
        errors = validate(path, *settings)
        if errors:
            failures += len(errors)
            for error in errors:
                print(f"ERROR: {path}: {error}")
        else:
            doc = json.loads(path.read_text(encoding="utf-8"))
            print(f"OK: {path}: {len(doc['mainSteps'])} steps")
    if failures:
        print(f"FAILED: {failures} SSM document validation problem(s)")
        return 1
    print(f"OK: validated {len(DOCUMENTS)} SSM Automation documents")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
