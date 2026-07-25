# IAM Guidance

The policies in [`policies/`](policies/) are reviewable examples for the individual response actions. Replace the example account IDs, user paths, bucket names, Regions, VPCs, and resource conditions before deployment.

## Principles

- Use one execution role per Lambda action.
- Keep read and write permissions in separate statements where AWS resource-level authorization permits it.
- Restrict S3 actions to approved bucket ARNs.
- Restrict IAM actions to a dedicated lab user path or explicit user ARNs.
- Restrict EC2 write actions by account, Region, resource tags, VPC, or permissions boundary where supported.
- Do not combine all example policies into a single broad responder role.
- Remember that the caller who invokes Lambda also needs `lambda:InvokeFunction`; that permission is separate from the function execution role.

Some EC2 describe operations and selected other APIs require `Resource: "*"`. This does not justify wildcard write permissions. Use identity policies, permission boundaries, service control policies, and explicit deployment variables together.

## Placeholder values

The standalone JSON examples intentionally use values such as:

```text
111122223333
arn:aws:s3:::example-incident-bucket-123
arn:aws:iam::111122223333:user/incident-lab/*
```

They are not ready to attach unchanged. Terraform generates account-aware execution policies and accepts explicit S3 bucket and IAM user ARN lists.
