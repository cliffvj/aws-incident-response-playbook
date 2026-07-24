#!/usr/bin/env bash
set -euo pipefail
function_name=${1:?usage: invoke_dry_run.sh FUNCTION_NAME EVENT_FILE}
event_file=${2:?usage: invoke_dry_run.sh FUNCTION_NAME EVENT_FILE}
aws sts get-caller-identity
aws lambda invoke --function-name "$function_name" --payload "fileb://$event_file" response.json
python3 -m json.tool response.json
