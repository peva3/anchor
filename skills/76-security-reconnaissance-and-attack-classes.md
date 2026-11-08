---
name: skill-76-security-reconnaissance-and-attack-classes
description: "Section 76 — Security Reconnaissance & Attack Classes. Load when scoping a security audit, choosing attack classes for a target type, or looking for what a checklist misses."
---
# Skill 76: Security Reconnaissance & Attack Classes

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 76. Security Reconnaissance & Attack Classes

Coverage is only as good as the unit list it starts from. Reconnaissance produces that list;
attack classes decide what each unit is tested for.

### 76.1 Map Before You Hunt

Write a one-page `architecture.md` before building the coverage ledger
([Section 75.2](skills/75-security-audit-loop.md)). Cap it at roughly 1,000 words and keep
it to source facts with `file:line` references:

1. **Product and principals** — who uses it, who operates it, what ordinary actions are
   trust-sensitive, and what resources are worth protecting.
2. **Stack and deployment** — languages, frameworks, build system, runtimes, and the
   deployment modes the repository actually selects.
3. **Entry surfaces** — HTTP/browser, RPC and messaging, files and archives, CLI/env/config,
   plugins and dependencies, cloud events, model context and tool arguments, mobile/deep
   links, local IPC.
4. **Trust boundaries** — each lower-trust principal and the strongest source-visible control
   on each boundary.
5. **Starting paths** — repository-relative files and subsystems a hunter should open first.
6. **Known limits** — missing toolchains, unobservable deployment facts, and anything that
   will have to stay `needs_validation`.

Reconnaissance reads source, tests, build files, and local manifests. It does not contact
deployed endpoints, identity providers, registries, brokers, or cloud APIs. Do not infer live
reachability from source; record it as an unobserved fact.

### 76.2 Choose Classes by Target Type

Select the classes that match the boundaries reconnaissance found. Do not select a class
because a language or dependency name appears — select it because the boundary it describes
is present.

| Target type | Classes to start from | Anchor context |
|-------------|-----------------------|----------------|
| Native, binary, kernel, firmware | Memory safety, integer/ABI, concurrency, binary loading, privileged interfaces | [53](skills/53-project-type-patterns.md) |
| AI, LLM, agents, MCP | Context and memory poisoning, action binding, tool-schema abuse, output handling | [55](skills/55-prompt-injection-defenses-for-agents.md) |
| HTTP, web, identity | Request framing, cache, sessions, CSRF, JWT/OAuth/OIDC/SAML, MFA, recovery and linking | [13](skills/13-security-best-practices.md), [31](skills/31-production-security-patterns.md) |
| Client-side, browser, extensions | DOM injection, messaging trust, UI redress, prototype pollution, storage and CORS | [63](skills/63-ui-quality-and-anti-slop-guardrails.md) |
| Supply chain and release | Dependency resolution, CI, signing, promotion, updates, plugins | [58](skills/58-supply-chain-security-and-sbom.md) |
| Cloud, IaC, containers | IAM, policy, workload identity, ingress, runtime configuration | [31](skills/31-production-security-patterns.md), [42](skills/42-infrastructure-as-code.md) |
| RPC, queues, streaming | Framing, serialization, replay, ordering, broker trust, webhooks | [12](skills/12-api-design.md) |
| Resource exhaustion | Shared CPU/memory/disk/connections, quotas, worker pools, operator spend | [29](skills/29-operational-patterns.md) |
| Data isolation and lifecycle | Tenant scope, caches, search, export/backup, migration, deletion, restore | [43](skills/43-database-backup-recovery.md) |
| Desktop, mobile, local IPC | Deep links, webview bridges, exported components, helpers, sockets | [53](skills/53-project-type-patterns.md) |

Split large targets by subsystem so one unit does not span unrelated trust boundaries.

### 76.3 High-Yield Classes Scanners Miss

Standard scanners find injection and known CVEs. These classes need a human-readable trace and
usually produce the highest-impact findings:

| Class | What to try |
|-------|-------------|
| **State-machine violation** | Skip a step, go backwards, replay a completed flow, leave a partial failure unreconciled |
| **Race with business impact** | Double-spend, double-approve, lost update, check-then-act across a non-atomic boundary |
| **Numeric manipulation** | Negative, zero, overflow, precision loss, string/number coercion in quantities and prices |
| **Export as exfiltration** | Low-privilege export or backup includes data above the caller's scope, deleted content, or history |
| **Import as injection** | Restore or import bypasses validation, overwrites other owners' data, or writes to collections the caller cannot write |
| **Search as oracle** | Filters, sort order, counts, or timing reveal existence, status, roles, or hidden field values |
| **Enumeration by side effect** | Error text, status codes, response size, or timing distinguish "not found" from "no access" |
| **Preview and draft leakage** | Preview tokens unlock more than one item; drafts leak through search, feeds, sitemaps, or cache headers |
| **Callback as SSRF** | User-supplied webhook, notification, or callback URL is fetched without egress validation, including after redirects |

For each, name the principal, the precondition, and the concrete result that would prove the
boundary failed. A pattern that looks wrong but cannot reach a result is a hardening note, not
a finding ([Section 75.6](skills/75-security-audit-loop.md)).

### 76.4 Assign the Wildcard

Reserve one unit with no assigned class. Its job is to find what the categories missed:

- The strangest code in the repo: why does it exist, and what happens if it is abused?
- Half-finished, experimental, compatibility, and fallback features — they received the least review.
- Calls the API permits but the client never makes. The UI constrains users; the API does not.
- Undocumented routes, parameters, headers, and config flags.
- Feature combinations that were never designed together (localization + preview + cache,
  import + plugins + webhooks, OAuth + impersonation + API keys).
- Git history: reverted security fixes, commented-out checks, secrets removed but still in history.
- Test files: what edge cases are conspicuously not tested?

The wildcard keeps the same evidence bar as every other class.

### 76.5 Run the Obvious-Things Pass

One literal pass for exposures everyone assumes someone else checked:

- Hardcoded passwords, keys, tokens, and `-----BEGIN` blocks in source.
- `TODO`/`FIXME`/`HACK` comments that mention auth, validation, or permissions.
- Debug or dev mode reachable in production by env var, query parameter, or header.
- Test, seed, or example credentials that still work.
- Unprotected `/debug`, `/admin`, `/test`, `/status`, `/env`, `/.env`, `/config`, `/metrics` endpoints.
- Committed `.env`, `credentials.json`, `*.pem`, and `*.key` files; a `.gitignore` that misses them.
- Unpinned dependencies and known CVEs in the lockfile.
- `eval`, `exec`, `Function()`, dynamic `import()`, and `child_process` with input.
- CORS wildcard, especially combined with credentials.
- Cookies missing `HttpOnly`, `Secure`, or `SameSite`.
- Open redirect parameters (`redirect`, `return`, `next`, `url`, `goto`).
- TLS not enforced; HTTP-only endpoints.
- Stack traces, internal paths, or SQL errors in production responses.

A flag is not a finding. Trace the value and the reachable impact before reporting one
([Section 75.3](skills/75-security-audit-loop.md)).

### 76.6 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Class list copied wholesale** | Waste on boundaries the target does not have | Select from reconnaissance ([76.2](#762-choose-classes-by-target-type)) |
| **No architecture summary** | Units are arbitrary and coverage is unarguable | One page before the ledger ([76.1](#761-map-before-you-hunt)) |
| **Language-based selection** | "It's Go, so memory safety" | Select by trust boundary |
| **Scanner-only audit** | Misses logic, race, and lifecycle classes | Add [76.3](#763-high-yield-classes-scanners-miss) |
| **No wildcard** | The checklist defines the answer | One unclassified unit ([76.4](#764-assign-the-wildcard)) |
| **Flag reported as finding** | Inflates the count and destroys trust | Trace the impact ([76.5](#765-run-the-obvious-things-pass)) |
| **Live probing during recon** | Touches shared systems without authorization | Source and local artifacts only |

### 76.7 Verification

- Does `architecture.md` name principals, protected resources, entry surfaces, and boundaries?
- Is every selected class justified by a boundary found in reconnaissance?
- Did a wildcard unit run, and did the obvious-things checklist cover every item?
- Does every high-yield candidate name a principal, a precondition, and a concrete result?
- Are unobservable deployment facts recorded for `needs_validation` instead of guessed?

---

## References

- Cloudflare, `security-audit` skill — https://github.com/cloudflare/security-audit-skill
- Cloudflare, "Build your own vulnerability harness" — https://blog.cloudflare.com/build-your-own-vulnerability-harness
