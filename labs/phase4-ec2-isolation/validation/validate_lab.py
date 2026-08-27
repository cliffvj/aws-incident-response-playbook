#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAB = ROOT / "labs" / "phase4-ec2-isolation"
TF = LAB / "terraform" / "main.tf"
PREP = LAB / "scripts" / "prepare_scenario.py"


def load_prepare_module():
    spec = importlib.util.spec_from_file_location("phase4_prepare_scenario", PREP)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load prepare_scenario.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ERROR: {message}")


def main() -> int:
    required = [
        LAB / "README.md",
        LAB / "architecture.md",
        LAB / "expected-results" / "README.md",
        LAB / "interview-notes.md",
        LAB / "troubleshooting.md",
        LAB / "generated" / ".gitignore",
        LAB / "events" / "sample-simulated-finding.json",
        LAB / "scripts" / "prepare_scenario.py",
        LAB / "scripts" / "inject_detection.py",
        LAB / "scripts" / "simulate_suspicious_activity.py",
        LAB / "scripts" / "verify_target.py",
        LAB / "scripts" / "verify_isolation.py",
        LAB / "terraform" / "main.tf",
        LAB / "terraform" / "variables.tf",
        LAB / "terraform" / "outputs.tf",
        LAB / "terraform" / "versions.tf",
        LAB / "terraform" / "terraform.tfvars.example",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    require(not missing, f"missing lab files: {missing}")

    text = TF.read_text(encoding="utf-8")
    checks = {
        "target must not define inbound security-group rules": re.search(r"\bingress\s*\{", text) is None,
        "lab event source must stay aws-ir.lab": re.search(r'source\s*=\s*\["aws-ir\.lab"\]', text) is not None,
        "lab detail type must stay simulated": '"Simulated Security Finding"' in text,
        "IMDSv2 must be required": re.search(r'http_tokens\s*=\s*"required"', text) is not None,
        "root EBS must be encrypted": re.search(r"encrypted\s*=\s*true", text) is not None,
        "target must have SSM core attachment": "AmazonSSMManagedInstanceCore" in text,
        "target must not define SSH port 22": re.search(r"from_port\s*=\s*22\b", text) is None,
    }
    for message, ok in checks.items():
        require(ok, message)

    sample = json.loads((LAB / "events" / "sample-simulated-finding.json").read_text(encoding="utf-8"))
    require(sample.get("source") == "aws-ir.lab", "sample source mismatch")
    require(sample.get("detail-type") == "Simulated Security Finding", "sample detail-type mismatch")
    require(sample.get("detail", {}).get("simulation") is True, "sample must be explicitly simulated")
    require(sample.get("detail", {}).get("scenario") == "phase4-ec2-isolation", "sample scenario mismatch")

    module = load_prepare_module()
    values = module.build_inputs(
        instance_id="i-0123456789abcdef0",
        account_id="111122223333",
        region="us-east-1",
        requested_by="validator",
        finding_id="phase4-ec2-isolation-simulated-001",
    )
    require(str(values["incident_id"]).startswith("EVT-"), "generated incident ID must use EVT prefix")
    require(values["detail"]["simulation"] is True, "generated detail must be simulated")
    require(values["containment"]["dry_run"] is False, "live containment input must be explicit")
    require(values["containment"]["expected_account_id"] == "111122223333", "account context mismatch")

    first = module.build_inputs(
        instance_id="i-0123456789abcdef0",
        account_id="111122223333",
        region="us-east-1",
        requested_by="validator",
        finding_id="phase4-ec2-isolation-simulated-001",
    )
    require(first["incident_id"] == values["incident_id"], "incident ID must be deterministic")

    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    require("**/.terraform/**" in ignore, "root .gitignore must exclude nested Terraform caches")
    require("**/__pycache__/" in ignore, "root .gitignore must exclude Python cache directories")

    print("OK: Phase 4 EC2 isolation lab structure, input contract, and safety checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
