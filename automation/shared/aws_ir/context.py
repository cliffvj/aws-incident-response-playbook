from __future__ import annotations
import os


def region_from(event: dict) -> str:
    return event.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
