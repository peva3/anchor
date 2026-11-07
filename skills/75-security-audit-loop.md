---
name: skill-75-security-audit-loop
description: "Section 75 — Security Audit Loop. Load when auditing a codebase or API for vulnerabilities, reviewing a change for security impact, or validating a reported finding."
---
# Skill 75: Security Audit Loop

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 75. Security Audit Loop

[Section 13](skills/13-security-best-practices.md) lists the controls to write.
This section is the method for proving which ones are present, where they fail, and how
confident you are. An audit that says "looks secure" without a coverage record is a guess.

### 75.1 An Audit Is a Method, Not a Checklist

A checklist run top-to-bottom answers "did I look at the usual things?" An audit answers
"what did I check, what did I not check, and what evidence supports each verdict?"

Three properties make the difference:

- **Enumerated coverage.** Every entry point and attack class is a unit, and every unit has
  a status.
- **Adversarial validation.** The person who finds a bug does not get to confirm it.
- **Tri-state verdicts.** A finding is confirmed, explicitly unresolved, or disproved — never
  "probably fine".

### 75.2 Build the Coverage Ledger

Enumerate the units before testing anything:

| Axis | Examples |
|------|----------|
| **Entry points** | HTTP routes, GraphQL resolvers, CLI commands, queue consumers, webhooks, file parsers, scheduled jobs, WebSocket handlers |
| **Trust boundaries** | Browser → API, service → service, tenant → tenant, user → admin, public → internal network |
| **Attack classes** | Authentication, authorization/IDOR, injection (SQL/NoSQL/command/template), SSRF, path traversal, unsafe deserialization, file upload, secrets exposure, crypto misuse, rate limiting/abuse, log injection, prompt injection (LLM surfaces) |

Ledger columns: `ID`, `entry point`, `trust boundary`, `attack class`, `status`
(`checked` / `not-checked` / `not-applicable`), `evidence`, `owner`.

- Enumerate entry points from the router/handler registration, not from memory.
- `not-applicable` needs a reason ("no file input on this endpoint").
- **`not-checked` is a finding, not a pass.** It belongs in the report with a reason.
- Run a **coverage critic** pass whose only job is to find missing units: an endpoint with
  no row, an attack class absent for a parser, a trust boundary nobody tested.

### 75.3 Trace Source to Sink

For each checked unit, record the path from untrusted input to the dangerous operation:

```
source:  POST /invoices  body.filter          (handler.go:42)
sink:    db.Query("... " + filter)            (repo.go:118)
control: none — string concatenation
verdict: confirmed injection (bounded observed result: query returns other tenant rows)
```

- No trace means `not-checked`, regardless of how the code "looks".
- Quote `file:line` for both source and sink. A finding without a path is a suspicion.
- Stop at the boundary of the claim: "checked the invoice routes; did not check the export
  worker" is honest and useful.

### 75.4 Validate Adversarially

- **The finder never confirms its own finding.** Spawn a fresh verifier with the finding and
  the code, whose instruction is to **disprove** it.
- The verifier gets a different prompt and, where possible, a fresh context. It does not see
  the finder's reasoning, only the claim and the evidence.
- If the verifier cannot reproduce the path, downgrade or reject the finding. Record why.
- This is the security instance of the independent-axes rule in
  [Section 70.4](skills/70-two-axis-code-review.md).

### 75.5 Use Tri-State Verdicts

| Verdict | Requires | Report shape |
|---------|----------|--------------|
| **Confirmed** | Source-to-sink trace plus a bounded observed result (a request, a test, a query returning data it should not) | Full finding with severity and fix |
| **Needs validation** | Exactly one named unresolved fact, and no severity assigned | "Needs validation: whether `tenant_id` is set before the query; cannot confirm without a database fixture" |
| **Rejected** | The disproof — why the path does not exist or the control holds | One line, kept so the next run does not re-investigate |

- Do not assign severity to `needs_validation`. Severity without confirmation is fiction.
- Do not drop rejected findings silently; the ledger is how the next audit saves time.

### 75.6 Severity and Hardening Notes

- **Severity = likelihood × impact**, given the actual preconditions. State the preconditions:
  "unauthenticated", "any tenant user", "requires a crafted file", "admin only".
- A missing defense-in-depth layer with no reachable path is a **hardening note**, not a
  vulnerability. Report it separately so it does not inflate the count.
- A confirmed issue with a trivial precondition outranks a theoretical chain that needs three
  unlikely conditions.
- Fix guidance names the control ([Section 13](skills/13-security-best-practices.md)) and the
  test that proves it.

### 75.7 Respect the Sandbox Gate

Never execute target code or a live exploit unless the environment provides an OS-enforced
sandbox (container, VM, seccomp, network isolation).

- No sandbox → static analysis only. Findings that would need execution stay
  `needs_validation`.
- Do not send payloads to production, shared staging, or a third-party service.
- Do not exfiltrate real data to prove a read. Use a bounded, synthetic marker where possible.
- Record the gate in the report: "dynamic validation unavailable; N findings need validation".

### 75.8 Audits Are Additive

- Reuse the previous ledger. Do not start from a blank page and call it a fresh audit.
- Revalidate units whose source changed; mark stale entries.
- **Never count a stale or unresolved unit as covered.** Coverage is a claim about this
  revision of the code.
- One pass finds roughly half of what repeated independent passes find. Say "one pass" when
  that is what you did, and schedule another rather than implying completeness.

### 75.9 Report Format

```markdown
## Coverage
Checked: 18 / 24 units (75%). Not checked: 4 (export worker, admin CLI, webhook retry,
SAML callback). Not applicable: 2.

## Confirmed
- [HIGH] `repo.go:118` — invoice filter concatenated into SQL. Preconditions: any
  authenticated tenant user. Evidence: request returns another tenant's rows.
  Fix: parameterize the query; add a cross-tenant test (Section 13, Section 31).

## Needs validation
- `auth/saml.go:77` — signature check may be skipped when `RelayState` is empty.
  Unresolved fact: whether the upstream middleware rejects empty RelayState.

## Rejected
- `upload.go:30` path traversal — filename is normalized and joined under the upload root.

## Hardening notes
- No rate limit on `/login`; not exploitable alone, but enables credential stuffing.
```

- Every confirmed finding has a path, a precondition, evidence, and a fix.
- The coverage line is mandatory. "No findings" without coverage is not a result.

### 75.10 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Checklist without coverage** | Sounds thorough, hides untouched surface | Ledger with explicit `not-checked` |
| **Finder confirms itself** | Motivated reasoning confirms false positives | Fresh adversarial verifier |
| **Severity on a guess** | Inflates the report and erodes trust | `needs validation`, no severity |
| **Grepping for `eval(` and calling it an audit** | Finds patterns, not reachable paths | Trace source to sink per unit |
| **Dynamic testing without a sandbox** | Risks the host and real data | Static only, or a real sandbox |
| **Fresh audit every time** | Re-investigates rejected findings | Additive ledger |
| **Counting unresolved as covered** | False completeness | Coverage is per revision and per verdict |

### 75.11 Verification

- Does the ledger enumerate entry points from the code, not memory?
- Does every unit have a status and evidence?
- Was every confirmed finding validated by someone other than its finder?
- Are `needs_validation` items severity-free and each tied to one unresolved fact?
- Is the sandbox gate recorded, with dynamic findings downgraded when it is absent?
- Does the report state coverage and what was not checked?

---

## References

- Cloudflare, `security-audit-skill` — https://github.com/cloudflare/security-audit-skill
