#!/usr/bin/env bash
set -euo pipefail
echo "AWS identity:"
aws sts get-caller-identity
echo "Configured Region: ${AWS_REGION:-${AWS_DEFAULT_REGION:-not-set}}"
echo "Profile: ${AWS_PROFILE:-default}"
