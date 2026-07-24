# Automation Architecture

```mermaid
flowchart LR
    O[Authorized operator or future orchestrator] --> V[Validate event contract]
    V --> D{dry_run?}
    D -->|true| P[Return planned action]
    D -->|false| A[Call scoped AWS API]
    A --> L[Structured CloudWatch log]
    A --> R[Structured action result]
    R --> O

    subgraph Actions
      M[Collect EC2 metadata]
      I[Isolate EC2]
      S[Snapshot EBS]
      K[Disable IAM key]
      N[Publish SNS update]
    end
```

The functions are deliberately independent. Step Functions orchestration, approval gates, EventBridge rules, and automated rollback are reserved for later Phase 3 commits.
