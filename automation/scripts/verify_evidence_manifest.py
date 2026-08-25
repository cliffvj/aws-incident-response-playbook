#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from urllib.parse import urlparse

import boto3


def parse_s3_uri(uri: str) -> tuple[str, str]:
    parsed = urlparse(uri)
    if parsed.scheme != "s3" or not parsed.netloc or not parsed.path.lstrip("/"):
        raise ValueError("manifest URI must be s3://bucket/key")
    return parsed.netloc, parsed.path.lstrip("/")


def digest_stream(body) -> str:
    value = hashlib.sha256()
    while True:
        chunk = body.read(1024 * 1024)
        if not chunk:
            break
        value.update(chunk)
    return value.hexdigest()


def canonical_index_sha256(objects: list[dict]) -> str:
    payload = json.dumps(objects, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify SSM evidence objects against an aws-ir evidence manifest.")
    parser.add_argument("manifest_uri", help="s3://bucket/.../integrity-manifest.json")
    args = parser.parse_args()

    try:
        bucket, key = parse_s3_uri(args.manifest_uri)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    s3 = boto3.client("s3")
    manifest_response = s3.get_object(Bucket=bucket, Key=key)
    manifest = json.loads(manifest_response["Body"].read())
    if manifest.get("schema") != "aws-ir-evidence-manifest/v1":
        print("ERROR: unsupported manifest schema", file=sys.stderr)
        return 2

    objects = manifest.get("objects", [])
    expected_index = manifest.get("evidence_index_sha256", "")
    actual_index = canonical_index_sha256(objects)
    failures = 0
    if actual_index != expected_index:
        print(f"FAIL evidence index: expected={expected_index} actual={actual_index}")
        failures += 1
    else:
        print(f"OK evidence index sha256={actual_index}")

    for item in objects:
        object_key = item["key"]
        try:
            response = s3.get_object(Bucket=bucket, Key=object_key)
            actual = digest_stream(response["Body"])
        except Exception as exc:  # boto3 error classes vary by operation/runtime
            print(f"FAIL {object_key}: {exc}")
            failures += 1
            continue
        expected = item["sha256"]
        if actual != expected:
            print(f"FAIL {object_key}: expected={expected} actual={actual}")
            failures += 1
        else:
            print(f"OK   {object_key} sha256={actual}")

    if failures:
        print(f"FAILED: {failures} verification problem(s)")
        return 1
    print(f"VERIFIED: {len(objects)} evidence object(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
