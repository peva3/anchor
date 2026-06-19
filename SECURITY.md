# Security Policy

## Reporting a Vulnerability

If you discover a vulnerability in this project, please report it privately. This template repository itself has minimal attack surface (it's mostly Markdown), but vulnerabilities can exist in:

- Code examples that contain security anti-patterns
- Instructions that could lead agents to make insecure choices
- Missing coverage of critical security domains

**Do NOT open a public issue for security vulnerabilities.**

Email: Create a security advisory via the GitHub Security tab.

## Supported Versions

The `main` branch is the only supported version. All security fixes are applied to main.

## What This Project Does for Security

The AGENTS.md template covers extensive security guidance for projects that adopt it:

| Section | Security Domain |
|---------|----------------|
| Section 13 | Security best practices — input validation, parameterized queries, rate limiting, secrets |
| Section 27.3 | Security constraints — SQL injection, eval/exec, path traversal, password hashing |
| Section 31.1 | Prompt injection detection — heuristic pre-filter, regex patterns, threat levels |
| Section 31.2 | Admin audit logging — IP, user agent, action tracking |
| Section 31.3 | API key encryption — Fernet-based at-rest encryption |
| Section 31.4 | Admin IP whitelist — network-level access control |
| Section 31.5 | Security CI/CD workflow — pip-audit, safety, auto-issue creation |
| Section 36 | Explicit NEVER list — 6 categories including code/git/GitHub/security prohibitions |
| Section 37 | Pre-commit hooks — detect-secrets, bandit, private key detection |
| Section 44 | Secrets management — tiered strategy, rotation, scanning |

## Known Security Gaps

We do not currently cover:

- Hardware security module (HSM) integration
- Binary/supply-chain signing and verification
- FIPS compliance requirements
- Zero-trust architecture patterns

If you identify a security domain not covered that leads to real-world vulnerabilities, please contribute (see CONTRIBUTING.md).
