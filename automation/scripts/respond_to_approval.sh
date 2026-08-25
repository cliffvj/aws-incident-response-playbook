#!/usr/bin/env bash
set -euo pipefail

DECISION="${1:-}"
case "$DECISION" in
  APPROVE|DENY) ;;
  *) echo "Usage: $0 APPROVE|DENY" >&2; exit 64 ;;
esac

read -r -s -p "Step Functions task token: " TASK_TOKEN
echo
read -r -p "Responder identifier: " RESPONDER
read -r -p "Comment (optional): " COMMENT

TASK_OUTPUT="$(python3 - "$DECISION" "$RESPONDER" "$COMMENT" <<'PY2'
import json, sys
print(json.dumps({"decision": sys.argv[1], "approved_by": sys.argv[2], "comment": sys.argv[3]}))
PY2
)"

aws stepfunctions send-task-success \
  --task-token "$TASK_TOKEN" \
  --task-output "$TASK_OUTPUT"

unset TASK_TOKEN TASK_OUTPUT
