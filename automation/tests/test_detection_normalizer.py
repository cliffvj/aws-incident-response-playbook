from __future__ import annotations
import importlib.util
import json
import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"detection"/"normalizer"/"app.py"
spec=importlib.util.spec_from_file_location("detection_normalizer", PATH)
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class DetectionNormalizerTests(TestCase):
    def setUp(self):
        self.env=patch.dict(os.environ, {
            "DEDUP_TABLE_NAME":"dedupe",
            "INCIDENT_TOPIC_ARN":"arn:aws:sns:us-east-1:111122223333:topic",
            "STATE_MACHINE_ARN":"arn:aws:states:us-east-1:111122223333:stateMachine:test",
            "DEFAULT_RESPONSE_ROUTE":"notify_only",
        }, clear=False)
        self.env.start()
    def tearDown(self): self.env.stop()

    def sample(self,name):
        return json.loads((ROOT/"detection"/"samples"/name).read_text(encoding="utf-8"))

    def test_guardduty_extracts_ec2_and_high_severity(self):
        item=mod._normalize(self.sample("guardduty-ec2-finding.json"))
        self.assertEqual(item["resource_id"],"i-0123456789abcdef0")
        self.assertEqual(item["severity"],"HIGH")

    def test_securityhub_extracts_ec2(self):
        item=mod._normalize(self.sample("securityhub-ec2-finding.json"))
        self.assertEqual(item["resource_type"],"ec2_instance")

    def test_cloudtrail_tampering_is_high(self):
        item=mod._normalize(self.sample("cloudtrail-stop-logging.json"))
        self.assertEqual(item["severity"],"HIGH")

    def test_non_ec2_triage_falls_back_to_notify(self):
        with patch.dict(os.environ,{"DEFAULT_RESPONSE_ROUTE":"triage"},clear=False):
            item=mod._normalize(self.sample("cloudwatch-alarm.json"))
            self.assertEqual(mod._route(item),"notify_only")

    def test_duplicate_stops_routing(self):
        event=self.sample("guardduty-ec2-finding.json")
        ddb=MagicMock(); sns=MagicMock(); sts=MagicMock()
        from botocore.exceptions import ClientError
        ddb.put_item.side_effect=ClientError({"Error":{"Code":"ConditionalCheckFailedException","Message":"duplicate"}},"PutItem")
        def factory(name,**kwargs):
            return {"dynamodb":ddb,"sns":sns,"stepfunctions":MagicMock()}[name]
        with patch.object(mod.boto3,"client",side_effect=factory):
            out=mod.handler(event, MagicMock(aws_request_id="x"))
        self.assertEqual(out["status"],"duplicate")
        sns.publish.assert_not_called()

    def test_notify_only_publishes_after_dedupe(self):
        event=self.sample("config-noncompliant.json")
        ddb=MagicMock(); sns=MagicMock(); sns.publish.return_value={"MessageId":"m-1"}
        def factory(name,**kwargs):
            return {"dynamodb":ddb,"sns":sns,"stepfunctions":MagicMock()}[name]
        with patch.object(mod.boto3,"client",side_effect=factory):
            out=mod.handler(event, MagicMock(aws_request_id="x"))
        self.assertEqual(out["route"],"notify_only")
        sns.publish.assert_called_once()

    def test_triage_starts_dry_run_workflow(self):
        event=self.sample("guardduty-ec2-finding.json")
        ddb=MagicMock(); states=MagicMock(); states.start_execution.return_value={"executionArn":"arn:exec"}
        with patch.dict(os.environ,{"DEFAULT_RESPONSE_ROUTE":"triage"},clear=False):
            def factory(name,**kwargs):
                return {"dynamodb":ddb,"sns":MagicMock(),"stepfunctions":states}[name]
            with patch.object(mod.boto3,"client",side_effect=factory):
                out=mod.handler(event, MagicMock(aws_request_id="x"))
        payload=json.loads(states.start_execution.call_args.kwargs["input"])
        self.assertTrue(payload["dry_run"])
        self.assertEqual(payload["mode"],"triage")
        self.assertEqual(out["route"],"triage")
