# Security Policy

## Supported version

The latest GitHub release is supported.

## Reporting

Please open a GitHub issue for non-sensitive bugs. For a vulnerability, use GitHub's private vulnerability reporting if available; do not post secrets, device names, serial numbers, private paths, or full system logs.

## Security boundary

PowerChime Guard is read-only. It prints optional fixed-domain preference commands but does not execute them. It uses no network, telemetry, privilege escalation, process termination, persistence, or arbitrary shell evaluation.
