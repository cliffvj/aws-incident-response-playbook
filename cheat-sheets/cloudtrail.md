# CloudTrail Cheat Sheet

**Use for:** AWS API timeline, identity attribution, configuration changes.

Key fields: `eventTime`, `eventSource`, `eventName`, `awsRegion`, `sourceIPAddress`, `userAgent`, `userIdentity`, `requestParameters`, `responseElements`, `errorCode`, `resources`.

Event history covers recent management events; use a trail or CloudTrail Lake/Athena-backed logs for durable, broader investigations. Verify all Regions and accounts.
