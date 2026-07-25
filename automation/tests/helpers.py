from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]


def load_action(name: str) -> ModuleType:
    path = ROOT / "lambda" / name / "app.py"
    spec = importlib.util.spec_from_file_location(f"test_action_{name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def context() -> MagicMock:
    value = MagicMock()
    value.aws_request_id = "request-123"
    return value


def client_router(**clients):
    def factory(service_name: str, **kwargs):
        if service_name not in clients:
            raise AssertionError(f"unexpected boto3 client: {service_name}")
        return clients[service_name]

    return factory


def sts(account_id: str = "111122223333") -> MagicMock:
    client = MagicMock()
    client.get_caller_identity.return_value = {
        "Account": account_id,
        "Arn": f"arn:aws:sts::{account_id}:assumed-role/test/session",
        "UserId": "AROATEST:session",
    }
    return client
