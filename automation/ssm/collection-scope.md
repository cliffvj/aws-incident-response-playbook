# SSM Evidence Collection Scope

This document defines what Phase 3 Commit 4 collects and, equally important, what it intentionally does not collect.

## Linux collection

| Category | Collection examples | Limits / cautions |
|---|---|---|
| Collection metadata | UTC time, incident ID, instance ID, Automation execution ID, hostname | No secrets should be placed in identifiers |
| OS / boot context | `uname`, `/etc/os-release`, `hostnamectl`, uptime | Read-only commands may still update normal system caches |
| Processes | PID, parent PID, account, state, start time, elapsed time, executable and arguments | Command arguments may contain sensitive values; protect evidence accordingly |
| Network | addresses, routes, listening/connected sockets, optional `lsof -i` | Tool availability varies by distribution |
| Services | systemd service units or legacy service status | No service start/stop/restart |
| Packages | RPM, dpkg, or apk inventory | Package history quality varies by distribution |
| Users / logons | passwd database, `who`, `w`, `last`, `lastlog` | `/etc/shadow` and password material are not collected |
| Scheduled tasks | systemd timers, cron configuration and per-user crontabs | Contents can include sensitive command parameters |
| Kernel / mounts | mount table, filesystem usage, loaded modules | No module unloading or mount changes |
| Recent file metadata | limited metadata under `/tmp` and `/var/tmp` | Names and metadata only; no arbitrary file bodies |
| Selected logs | bounded journal and common auth/system log tails | Not a substitute for centralized immutable logs |

## Windows collection

| Category | Collection examples | Limits / cautions |
|---|---|---|
| Collection metadata | UTC time, incident ID, instance ID, Automation execution ID, computer name | No secrets in identifiers |
| OS context | operating-system and computer information | Read-only WMI/CIM/PowerShell queries |
| Processes | PID, parent PID, image name/path, creation date | Command lines are intentionally omitted by default |
| Network | IP addresses, routes, TCP connections | No firewall or interface changes |
| Services | service state and identity | No service changes |
| Software / updates | installed hotfixes and uninstall registry metadata | Avoids `Win32_Product` because it can trigger installer consistency actions |
| Users / logons | local users, current token, terminal sessions | No credential extraction |
| Scheduled tasks | task path/name/state/author | Task action bodies are not expanded in this baseline |
| Selected logs | bounded System, Application, and Security events from the last 24 hours | Event messages can contain sensitive data |

## Intentionally excluded

This commit does **not** attempt to collect:

- volatile memory or memory dumps;
- deleted-file recovery or unallocated disk space;
- full EBS forensic images (use the snapshot workflow instead);
- browser stores, password databases, secrets, private keys, or credential dumping artifacts;
- process environment blocks;
- arbitrary application data;
- every log file on the host;
- malware detonation or active scanning;
- host isolation, patching, remediation, service termination, or file deletion.

Use [EBS snapshot and forensic preservation](../../docs/19-ebs-snapshot-forensic-preservation.md) when storage evidence is required, and follow organization-specific forensic tooling for memory or legal-evidence workflows.
