#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import boto3

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description="Invoke the deployed detection normalizer with a repository sample.")
parser.add_argument("--function-name", required=True)
parser.add_argument("--sample", default="guardduty-ec2-finding.json")
parser.add_argument("--region", default=None)
args=parser.parse_args()
path=ROOT/"detection"/"samples"/args.sample
payload=path.read_bytes()
client=boto3.client("lambda", region_name=args.region)
response=client.invoke(FunctionName=args.function_name, InvocationType="RequestResponse", Payload=payload)
print(response["Payload"].read().decode("utf-8"))
