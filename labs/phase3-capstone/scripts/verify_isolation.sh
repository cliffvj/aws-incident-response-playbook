#!/usr/bin/env bash
set -euo pipefail
[[ $# -eq 2 ]] || { echo "Usage: $0 <instance-id> <incident-id>" >&2; exit 64; }
INSTANCE_ID="$1"
INCIDENT_ID="$2"
GROUP_NAME="aws-ir-quarantine-${INCIDENT_ID//[^A-Za-z0-9._-]/-}"
GROUP_NAME="${GROUP_NAME:0:255}"
aws ec2 describe-network-interfaces --filters "Name=attachment.instance-id,Values=$INSTANCE_ID" \
  --query 'NetworkInterfaces[].{ENI:NetworkInterfaceId,Groups:Groups[].{Id:GroupId,Name:GroupName}}' --output table
python3 - "$INSTANCE_ID" "$GROUP_NAME" <<'PYVERIFY'
import json, subprocess, sys
instance_id, expected_name = sys.argv[1:]
data=json.loads(subprocess.check_output(['aws','ec2','describe-network-interfaces','--filters',f'Name=attachment.instance-id,Values={instance_id}','--output','json'], text=True))
enis=data.get('NetworkInterfaces',[])
if not enis: raise SystemExit('ERROR: no network interfaces found for target')
for eni in enis:
    names=[g.get('GroupName') for g in eni.get('Groups',[])]
    if names != [expected_name]: raise SystemExit(f"ERROR: {eni.get('NetworkInterfaceId')} is not isolated: {names}")
print(f"OK: all {len(enis)} target network interface(s) use only {expected_name}")
PYVERIFY
