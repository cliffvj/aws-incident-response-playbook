#!/usr/bin/env bash
set -euo pipefail

function_name=${1:?usage: invoke_dry_run.sh FUNCTION_NAME EVENT_FILE [OUTPUT_FILE]}
event_file=${2:?usage: invoke_dry_run.sh FUNCTION_NAME EVENT_FILE [OUTPUT_FILE]}
output_file=${3:-response.json}

python3 -m json.tool "$event_file" >/dev/null
if ! python3 - "$event_file" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as handle:
    event=json.load(handle)
if event.get("dry_run", True) is not True:
    raise SystemExit("refusing invocation: event dry_run must be true or omitted")
PY
then
  exit 1
fi

aws sts get-caller-identity
aws lambda invoke \
  --function-name "$function_name" \
  --cli-binary-format raw-in-base64-out \
  --payload "fileb://$event_file" \
  "$output_file"
python3 -m json.tool "$output_file"
