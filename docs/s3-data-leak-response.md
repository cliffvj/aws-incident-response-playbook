# S3 Data Leak Response

1. Record policies, ACLs, access points, Block Public Access, Object Ownership, encryption, versioning, replication, logging, and affected keys.
2. Contain unintended access without destroying access evidence.
3. Query CloudTrail management events and data events/access logs when available.
4. Determine exposure duration, principals, anonymous requests, object sensitivity, and downloads.
5. Rotate secrets contained in objects and restore changed/deleted objects from trusted versions or backups.
6. Add Config detection, least-privilege resource policies, and protected logging.
