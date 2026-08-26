#!/usr/bin/env bash
set -euo pipefail
DETAIL_FILE="${1:-labs/phase3-capstone/generated/event-detail.json}"
[[ -f "$DETAIL_FILE" ]] || { echo "ERROR: detail file not found: $DETAIL_FILE" >&2; exit 66; }
DETAIL_JSON="$(python3 - "$DETAIL_FILE" <<'PYDETAIL'
import json, sys
print(json.dumps(json.load(open(sys.argv[1], encoding='utf-8')), separators=(',', ':')))
PYDETAIL
)"
aws events put-events --entries "$(python3 - "$DETAIL_JSON" <<'PYENTRY'
import json, sys
print(json.dumps([{'Source':'aws-ir.lab','DetailType':'Simulated Security Finding','Detail':sys.argv[1]}]))
PYENTRY
)"
