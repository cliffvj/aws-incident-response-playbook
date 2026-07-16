-- Athena CloudTrail investigation query library
-- Replace cloudtrail_logs and timestamps with your table and incident window.

-- 1. Activity by access key
SELECT eventtime, eventsource, eventname, awsregion, sourceipaddress, useragent, errorcode, requestparameters
FROM cloudtrail_logs
WHERE useridentity.accesskeyid = 'AKIAEXAMPLE'
  AND from_iso8601_timestamp(eventtime) BETWEEN timestamp '2026-01-01 00:00:00' AND timestamp '2026-01-02 00:00:00'
ORDER BY eventtime;

-- 2. IAM persistence and privilege changes
SELECT eventtime, useridentity.arn, eventname, sourceipaddress, requestparameters
FROM cloudtrail_logs
WHERE eventsource = 'iam.amazonaws.com'
  AND eventname IN ('CreateUser','CreateAccessKey','CreateLoginProfile','CreateRole','AttachUserPolicy','AttachRolePolicy','PutUserPolicy','PutRolePolicy','UpdateAssumeRolePolicy','CreatePolicyVersion','SetDefaultPolicyVersion')
ORDER BY eventtime DESC;

-- 3. CloudTrail tampering
SELECT eventtime, useridentity.arn, eventname, sourceipaddress, requestparameters
FROM cloudtrail_logs
WHERE eventsource = 'cloudtrail.amazonaws.com'
  AND eventname IN ('StopLogging','DeleteTrail','UpdateTrail','PutEventSelectors','PutInsightSelectors')
ORDER BY eventtime DESC;

-- 4. Security-group changes
SELECT eventtime, useridentity.arn, eventname, sourceipaddress, requestparameters
FROM cloudtrail_logs
WHERE eventsource = 'ec2.amazonaws.com'
  AND eventname IN ('AuthorizeSecurityGroupIngress','AuthorizeSecurityGroupEgress','RevokeSecurityGroupIngress','RevokeSecurityGroupEgress','ModifySecurityGroupRules')
ORDER BY eventtime DESC;

-- 5. Anonymous S3 GetObject requests (requires appropriate S3 data events in the table)
SELECT eventtime, requestparameters, sourceipaddress, useragent
FROM cloudtrail_logs
WHERE eventsource = 's3.amazonaws.com'
  AND eventname = 'GetObject'
  AND useridentity.accountid = 'anonymous'
  AND useridentity.arn IS NULL
ORDER BY eventtime DESC;
