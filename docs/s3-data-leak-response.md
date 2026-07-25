# S3 Data Leak Response

1. Record policies, ACLs, access points, Block Public Access, Object Ownership, encryption, versioning, replication, logging, and affected keys.
2. Contain unintended access without destroying access evidence.
3. Query CloudTrail management events and data events/access logs when available.
4. Determine exposure duration, principals, anonymous requests, object sensitivity, and downloads.
5. Rotate secrets contained in objects and restore changed/deleted objects from trusted versions or backups.
6. Add Config detection, least-privilege resource policies, and protected logging.

## Automation references

- [Inspect S3 public-access state](../automation/lambda/inspect_s3_public_access/README.md)
- [Contain S3 public access](../automation/lambda/contain_s3_public_access/README.md)
- [Restore captured Block Public Access state](../automation/lambda/restore_s3_public_access/README.md)
- [S3 response action sequence](../automation/docs/response-actions.md#s3-public-access-sequence)
