# Initial Triage Checklist

- [ ] Assign incident ID, severity, commander, scribe, and technical lead.
- [ ] Record current UTC time, detection source, account, Region, and affected resources.
- [ ] Confirm responder identity with `aws sts get-caller-identity`.
- [ ] Determine whether activity is ongoing and whether data or critical operations are at risk.
- [ ] Preserve alerts, CloudTrail events, logs, configurations, and relevant screenshots/exports.
- [ ] Identify owners, dependencies, Auto Scaling/load-balancing membership, and blast radius.
- [ ] Select the least disruptive effective containment action and define rollback.
- [ ] Start an action log; never rely on memory or chat alone.
- [ ] Escalate legal, privacy, HR, fraud, communications, and AWS Support as required.
