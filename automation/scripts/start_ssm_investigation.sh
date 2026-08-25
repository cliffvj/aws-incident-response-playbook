#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  automation/scripts/start_ssm_investigation.sh <linux|windows> <instance-id> <incident-id>

Optional environment overrides:
  SSM_DOCUMENT_NAME
  SSM_AUTOMATION_ROLE_ARN
  SSM_EVIDENCE_BUCKET
  AWS_PROFILE / AWS_REGION / AWS_DEFAULT_REGION

Without overrides, the helper reads the corresponding values from
automation/terraform outputs.
EOF
}

if [[ $# -ne 3 ]]; then
  usage >&2
  exit 2
fi

platform="${1,,}"
instance_id="$2"
incident_id="$3"
case "$platform" in
  linux|windows) ;;
  *) echo "ERROR: platform must be linux or windows" >&2; exit 2 ;;
esac

if [[ ! "$instance_id" =~ ^i-[0-9a-fA-F]{8}([0-9a-fA-F]{9})?$ ]]; then
  echo "ERROR: invalid EC2 instance ID: $instance_id" >&2
  exit 2
fi
if [[ ! "$incident_id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{2,63}$ ]]; then
  echo "ERROR: invalid incident ID format" >&2
  exit 2
fi

output_name="ssm_${platform}_document_name"
document_name="${SSM_DOCUMENT_NAME:-$(terraform -chdir=automation/terraform output -raw "$output_name")}"
automation_role="${SSM_AUTOMATION_ROLE_ARN:-$(terraform -chdir=automation/terraform output -raw ssm_automation_role_arn)}"
evidence_bucket="${SSM_EVIDENCE_BUCKET:-$(terraform -chdir=automation/terraform output -raw ssm_evidence_bucket_name)}"
evidence_prefix="incidents"

# Trim accidental whitespace from command substitutions.
document_name="${document_name//[[:space:]]/}"
automation_role="${automation_role//[[:space:]]/}"
evidence_bucket="${evidence_bucket//[[:space:]]/}"

account_id="$(aws sts get-caller-identity --query Account --output text)"
region="${AWS_REGION:-${AWS_DEFAULT_REGION:-$(aws configure get region 2>/dev/null || true)}}"
if [[ -z "$region" ]]; then
  echo "ERROR: set AWS_REGION/AWS_DEFAULT_REGION or configure a CLI default Region" >&2
  exit 2
fi

printf 'AWS account : %s\n' "$account_id"
printf 'AWS Region  : %s\n' "$region"
printf 'Document    : %s\n' "$document_name"
printf 'Instance    : %s\n' "$instance_id"
printf 'Incident    : %s\n' "$incident_id"
printf 'Evidence    : s3://%s/%s/%s/%s/\n' "$evidence_bucket" "$evidence_prefix" "$incident_id" "$instance_id"

execution_id="$(aws ssm start-automation-execution \
  --document-name "$document_name" \
  --parameters \
    "AutomationAssumeRole=$automation_role,InstanceId=$instance_id,IncidentId=$incident_id,EvidenceBucket=$evidence_bucket,EvidencePrefix=$evidence_prefix" \
  --query AutomationExecutionId \
  --output text)"

printf '\nAutomationExecutionId: %s\n' "$execution_id"
printf 'Inspect with:\n  aws ssm get-automation-execution --automation-execution-id %s\n' "$execution_id"
printf 'Expected evidence prefix:\n  s3://%s/%s/%s/%s/%s/%s/\n' \
  "$evidence_bucket" "$evidence_prefix" "$incident_id" "$instance_id" "$execution_id" "$platform"
