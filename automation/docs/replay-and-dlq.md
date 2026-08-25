# Detection DLQ and replay

EventBridge retries target delivery for retriable failures. The reference Terraform target configuration uses a bounded retry window and an SQS dead-letter queue so undelivered events are not silently lost.

## DLQ workflow

1. Inspect the queue depth and oldest-message age.
2. Receive a message without deleting it.
3. Confirm the event source, account, Region, resource, and incident relevance.
4. Correct the target-side failure first.
5. Re-submit only after confirming the event will not cause duplicate or unsafe action.
6. Delete the DLQ message only after successful processing and incident correlation.

The normalizer deduplication key may intentionally treat a replay as a duplicate. For controlled replay testing, wait for the TTL window or remove only the exact test key from the dedicated lab table.

## EventBridge archive

`enable_detection_event_archive` is disabled by default because archives add cost and retention obligations. When enabled, matched source events are retained for `detection_archive_retention_days` and can be replayed using EventBridge archive/replay tooling.

## Important boundary

A replay should never be used to bypass a human approval gate. The detection layer can notify or start read-only triage; live containment remains a separate authorization decision.
