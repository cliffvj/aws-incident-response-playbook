# IAM Guidance

Policies in this directory are examples to review, narrow, and test. Some EC2 describe actions require `Resource: "*"`; write actions are separated so deployment roles can be independently assigned and constrained with tags or permissions boundaries.

Do not attach all policy examples to one role in production. Terraform creates one execution role per function.
