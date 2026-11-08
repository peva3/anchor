---
name: skill-77-security-finding-validation-and-reporting
description: "Section 77 — Security Finding Validation & Reporting. Load after hunting, before writing findings or reports, when carrying prior audit results, or when a finding must be independently verified."
---
# Skill 77: Security Finding Validation & Reporting

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 77. Security Finding Validation & Reporting

Finding a candidate is halfway. A finding earns trust when an independent reviewer can
reproduce the record and a reader can act on it without re-deriving the evidence.

### 77.1 Verify the Written Record

Candidate validation ([Section 75.4](skills/75-security-audit-loop.md)) proves the bug exists.
Record verification proves the *report* is true. Use a fresh reviewer that did not hunt and
did not write the record.

For every `confirmed` record, re-check:

1. Every `file:line`, scope, and described operation in the trace.
2. That the first entry is a real lower-trust interface and the last is the claimed sink.
3. Every precondition, control on the path, and bounded observed result.
4. The affected principal and resource, and that the demonstrated impact matches the claim.
5. That severity is not greater than the demonstrated impact.
6. That the remediation enforces the invariant instead of moving trust elsewhere.

For every `needs_validation` record, re-check that the source path is real, each blocker is
decisive and not answerable locally, and at least one exact resolution step exists.

- The verifier returns **verified** or a **replacement record**, not prose.
- A replacement that promotes a verdict, changes the root cause, the trace, the observed
  result, the impact, or the severity needs **another** independent verifier. A record never
  promotes itself.
- Discard malformed or prose-wrapped results without repairing them; re-run with a fresh
  reviewer when budget allows. Otherwise leave the candidate in the ledger as unresolved.
- After any replacement, re-run the record validator ([77.3](#773-record-findings-as-data)).

### 77.2 Carry Prior Findings Correctly

A previous audit is evidence to re-check, not a cache to trust. Classify every prior unit
before assigning new work:

| Prior state | Current action |
|-------------|----------------|
| **Confirmed, same source** | Re-check the cited source; carry only if the trace, conditions, and evidence still hold |
| **Confirmed, changed source** | New revalidation unit — do not exclude the root cause from hunting |
| **Needs validation** | Keep the same blocker until the named fact is resolved; re-check its source trace |
| **Rejected** | Suppress only that exact claim, not the whole coverage unit |
| **Deferred / out of scope** | Becomes current work when it is now in scope |
| **Missing or incompatible ledger** | Record the gap; never treat it as empty coverage |

- A carried confirmation is verified again ([77.1](#771-verify-the-written-record)); the
  re-check is the unit's first check, not a free pass.
- Reuse prior paths, controls, and fingerprints to target work, never to skip it.
- Record what was carried, what was reopened, and why in the report.

### 77.3 Record Findings as Data

When an audit produces more than a handful of findings, separate the record from the prose:

- Write `findings.json` (or CSV) with three explicit branches:
  `confirmed` (trace, conditions, execution, observed result, severity, remediation),
  `needs_validation` (claimed cause, trace, evidence, exact blockers, resolution plan), and
  `rejected` (claimed cause, trace, evidence, disproof).
- Give every record a stable fingerprint for its root cause so runs can be compared.
- Keep severity out of `needs_validation`. Keep remediation out of `rejected`.
- Validate the data against a schema when it is written and again after every replacement.
  A validator proves shape and consistency, not that the finding is real.
- Derive `REPORT.md` and any detail files from the validated records. Prose never changes a
  verdict, severity, blocker, or observed result.
- A small audit may use a table instead of JSON — but it still keeps the three branches
  distinct and cites evidence per row.

### 77.4 Report in the Target's Native Interface

HTTP is one interface, not the default. Describe the bounded reproduction in the target's own
terms:

| Target | Native reproduction |
|--------|---------------------|
| Library | A function call with the documented input shape |
| Parser or format | A fixture file and the parse entry point |
| CLI | A command with arguments and exit behavior |
| Desktop or mobile | An IPC message, deep link, or exported component call |
| Service or API | A request, message, or resolver invocation |
| Infrastructure | A locally rendered policy or plan showing the effective permission |

Do not require an endpoint, account, or live environment the target does not have. Do not send
audit traffic to a deployment ([Section 75.7](skills/75-security-audit-loop.md)).

### 77.5 Report Structure and Honesty

A complete report has these sections, in this order:

1. **Run status** — scope profile, what was in and out of scope, what was deferred, prior-run
   use, sandbox limits, and an explicit `complete` or `incomplete` status.
2. **Posture** — a short summary of the trust boundaries and the strongest controls.
3. **Confirmed** — a table (severity, title, boundary, observed result) and one detail block
   per finding: trace, principal, bounded reproduction, conditions, impact, smallest fix.
4. **Needs validation** — a separate table with the trace, exact blocker, and the bounded local
   or owner-observed step that would resolve it. No severity.
5. **Hardening notes and positive patterns** — defense-in-depth gaps with no reachable path,
   and controls worth keeping.
6. **Coverage** — covered, candidate, blocked, and deferred counts from the ledger, plus the
   important exclusions and the coverage critic's result.

- **Zero confirmed findings is a valid result.** State it with the coverage and validation
  limits; never invent a LOW finding to fill the report.
- Rejected records are not findings. Mention a fingerprint only when it explains a prior
  disagreement or a coverage decision.
- A quick, scoped, or budget-limited run is a **partial pass**; say so plainly.
- Do not describe an unvalidated candidate as a finding.

### 77.6 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Hunter verifies its own record** | Confirmation bias with a citation | Fresh reviewer ([77.1](#771-verify-the-written-record)) |
| **Prose as the source of truth** | Numbers drift between summary and detail | Data first, prose derived ([77.3](#773-record-findings-as-data)) |
| **Severity on unresolved leads** | Turns a question into a fake fact | No severity until confirmed |
| **Reusing a prior pass as coverage** | Stale evidence presented as current | Re-check per [77.2](#772-carry-prior-findings-correctly) |
| **HTTP assumed** | Invents an interface the target lacks | Native reproduction ([77.4](#774-report-in-the-targets-native-interface)) |
| **Filling a clean report** | Manufactures findings to look useful | Report zero honestly ([77.5](#775-report-structure-and-honesty)) |
| **Burying rejected work** | The next run repeats it | Keep the disproof and fingerprint |

### 77.7 Verification

- Did a reviewer who did not hunt verify every retained record?
- Were material replacements verified by a second independent reviewer?
- Is every prior unit classified and either re-checked or explicitly reopened?
- Do the records validate against the schema, and does the prose match the records exactly?
- Is each reproduction written in the target's native interface?
- Does the report state its status, scope, limits, and coverage counts?

---

## References

- Cloudflare, `security-audit` skill — https://github.com/cloudflare/security-audit-skill
- Cloudflare, "Build your own vulnerability harness" — https://blog.cloudflare.com/build-your-own-vulnerability-harness
