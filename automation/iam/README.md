# IAM Guidance

Policies under [`policies/`](policies/) are reviewable examples for individual response actions and the Step Functions approval callback. Replace sample scopes before deployment.

## Principles

- Use one execution role per Lambda action.
- Use a separate Step Functions execution role for orchestration.
- Do not attach the approver callback policy to the state-machine role or general users.
- Restrict S3 actions to approved bucket ARNs and IAM actions to approved users/paths.
- Restrict EC2 write actions with account, Region, resource tags, VPC constraints, permissions boundaries, and organizational controls where supported.
- Keep automatic finding triggers separate from response actions until their routing and suppression logic is explicitly tested.

## Callback-policy wildcard

[`policies/step-functions-approver-policy.json`](policies/step-functions-approver-policy.json) uses `Resource: "*"` for `states:SendTaskSuccess` and `states:SendTaskFailure`. AWS Step Functions callback APIs are authorized by possession of the task token and these IAM actions do not provide a state-machine resource type for resource-level scoping.

Because the resource cannot be narrowed in the identity policy, compensate operationally:

- attach the policy only to a dedicated, strongly authenticated approver role;
- distribute task tokens only through the dedicated approval channel;
- keep token-bearing messages out of general chat and ticket systems;
- use short approval timeouts; and
- monitor CloudTrail for callback activity.

The Terraform approver policy is created for review but **not attached automatically**.

## Placeholder values

Standalone JSON policies and samples use values such as `111122223333`, `example-incident-bucket-123`, and `incident-lab/*`. They are not ready to attach unchanged.
