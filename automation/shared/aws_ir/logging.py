from __future__ import annotations
import json, logging
from typing import Any

LOGGER = logging.getLogger("aws_ir")
LOGGER.setLevel(logging.INFO)


def log(event: str, **fields: Any) -> None:
    LOGGER.info(json.dumps({"event": event, **fields}, default=str, sort_keys=True))
