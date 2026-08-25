#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <state-machine-arn> <event-json>" >&2
  exit 64
fi

STATE_MACHINE_ARN="$1"
EVENT_FILE="$2"

if [[ ! -f "$EVENT_FILE" ]]; then
  echo "Event file not found: $EVENT_FILE" >&2
  exit 66
fi

aws sts get-caller-identity
aws stepfunctions start-execution \
  --state-machine-arn "$STATE_MACHINE_ARN" \
  --input "file://$EVENT_FILE"
