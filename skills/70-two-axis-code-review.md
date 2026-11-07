---
name: skill-70-two-axis-code-review
description: "Section 70 — Two-Axis Code Review. Load when reviewing a pull request or diff for both standards compliance and spec correctness."
---
# Skill 70: Two-Axis Code Review

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 70. Two-Axis Code Review

A review answers two different questions, and mixing them produces a muddled report:

- **Standards** — is this code good, by the rules this repo documents?
- **Spec** — does this code do what the task required?

Run the axes independently, in parallel where possible, and report them separately. A
finding on one axis must not be re-ranked or suppressed because of the other.

### 70.1 Pin the Review Boundary

Review a fixed diff, not the working tree:

```bash
git diff --stat <base>...HEAD
git diff <base>...HEAD
git log --oneline <base>..HEAD
```

Use the merge-base (`...`) so unrelated changes on the base branch do not appear. Record
the base commit in the report; "reviewed the PR" without a fixed point is unrepeatable.
For a self-review before commit, the base is `HEAD`.

**Then read the blast radius.** The diff is the change; the callers are the consequence.
For every changed public function, type, schema, or config key, read at least one caller and
the nearest test. A review that reads only the diff cannot see the broken contract.

### 70.2 Axis A — Standards

Check the repo's documented rules **first**; they override any generic taste. Then use the
smell baseline below as a checklist, not a scorecard.

| Smell | What it looks like | Usual fix |
|-------|--------------------|-----------|
| **Mysterious Name** | `data`, `tmp`, `handle2` | Rename to the domain concept |
| **Duplicated Code** | Same branch in two places | Extract the shared rule |
| **Feature Envy** | A method reads another object's fields | Move the behavior |
| **Data Clumps** | The same 4 parameters travel together | Introduce a type |
| **Primitive Obsession** | Strings for IDs, money, units | Value object or typed ID |
| **Repeated Switches** | Same `switch` in several files | Polymorphism or one table |
| **Shotgun Surgery** | One change touches many files | Gather the responsibility |
| **Divergent Change** | One file changes for unrelated reasons | Split by reason to change |
| **Speculative Generality** | Hooks and parameters nobody uses | Delete until needed ([Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md)) |
| **Message Chains** | `a.b().c().d()` | Ask the object for the result |
| **Middle Man** | A class that only delegates | Remove or collapse it |
| **Refused Bequest** | A subclass ignores most of its parent | Prefer composition |

Also check the hard rules that are cheap to verify: tests exist and assert behavior
([Section 8](skills/08-testing-requirements.md)), no secrets
([Section 44](skills/44-secrets-management.md)), error paths are handled
([Section 10](skills/10-error-handling-patterns.md)), and the diff respects the size limit
([Section 33](skills/33-pr-change-size-standards.md)).

**Report only judgement calls that matter.** A smell is a prompt to look, not a defect by
itself. Cite the rule or smell for every finding.

### 70.3 Axis B — Spec

Compare the diff against the written spec ([Section 68](skills/68-spec-and-ticket-decomposition.md))
or, if none exists, against the original request. Check for:

- **Missing requirement** — the spec says it, the diff does not do it.
- **Partial requirement** — the happy path exists, the empty/error/permission path does not.
- **Scope creep** — behavior the spec did not ask for, especially new config or endpoints.
- **Wrong implementation** — the behavior is present but violates a constraint (format,
  ordering, idempotency, compatibility).
- **Unverified acceptance** — the stated check was not run, or does not prove the claim.

If there is no spec and the request was ambiguous, **that is a finding**: the review cannot
confirm correctness against a moving target. Point back to
[Section 67](skills/67-requirements-elicitation-grilling.md).

### 70.4 Keep the Axes Independent

- Run Standards and Spec as **separate passes** — separate subagents when the harness
  supports it ([Section 22](skills/22-multi-agent-cooperation-patterns.md)).
- Give each pass only what it needs: Standards gets the diff and the repo rules; Spec gets
  the diff and the spec/acceptance criteria.
- **Do not let one axis excuse the other.** "The code is beautiful but does not meet the
  spec" and "it meets the spec but is unmaintainable" are both failures.
- Report in two sections, with severities local to each axis. Do not produce one combined
  ranked list.
- **Sequence: Spec first, Standards second.** Confirm the change does the right thing before
  polishing how it does it. A beautiful implementation of the wrong requirement is rework.
- For a multi-task plan, review each slice against its own acceptance item as it lands, not
  only the combined diff at the end
  ([Section 68](skills/68-spec-and-ticket-decomposition.md)).

### 70.5 Report Format

```markdown
## Standards
- [BLOCKER] `src/cache.py:41` — cache key omits tenant ID (Section 31, tenant isolation).
  Fix: include the tenant in the key and add a cross-tenant test.
- [SHOULD] `src/api.py:88` — duplicated pagination branch (Duplicated Code).
  Fix: extract `paginate(query, cursor)`.

## Spec
- [BLOCKER] Missing: expired holds are never released (acceptance item 3).
- [SHOULD] Scope creep: new `admin_export` endpoint is not in the spec; split it out.

## Verdict
Standards: changes requested. Spec: not met (1 blocker).
```

Every finding needs **location, evidence, why it matters, what happens if you skip it, and
the fix**. A finding without a location is unactionable. A finding without a rule or spec
reference is taste. A finding without a consequence is a preference.

### 70.6 Verify Before You Report

- Re-read the diff around each finding; confirm the code actually does what you think.
- Drop findings that depend on code outside the pinned diff, unless you checked it.
- Do not invent line numbers or files — quote what is there.
- Separate **blockers** (correctness, security, spec) from **suggestions** (naming, style).
- If you found nothing on an axis, say so explicitly; silence is not a clean bill of health.
- **When you receive a review, verify before you comply.** Reproduce each point against the
  code; if it is valid, fix it, and if it is not, say why with evidence. Applying a
  plausible-sounding suggestion unchecked is how a review introduces a bug.

### 70.7 When to Use

| Situation | Both axes? | Notes |
|-----------|------------|-------|
| PR review | Yes | The default |
| Self-review before commit | Yes, quickly | Cheaper than a review cycle |
| AI-generated change | Yes | Standards catches slop ([Section 34](skills/34-ai-code-quality-anti-pattern-detection.md)) |
| Hotfix under incident | Spec first, Standards after | Restore service, then clean up |
| Documentation-only diff | Spec only | Standards reduce to links and accuracy |

### 70.8 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **One merged list** | Spec failures get buried under style nits | Two sections, two severities |
| **Style-only review** | A clean diff that misses the requirement | Always run the Spec axis |
| **Spec-only review** | Ships unmaintainable code | Always run the Standards axis |
| **Reviewing the branch tip** | Includes unrelated base changes | Pin `<base>...HEAD` |
| **Uncited findings** | Indistinguishable from taste | Cite rule, smell, or acceptance item |
| **Rubber stamp** | "LGTM" with no evidence | State what you checked and what you did not |

### 70.9 Verification

- Is the base commit recorded, and the diff reproducible?
- Did both axes run, with separate reports?
- Does every blocker name a location and a rule or acceptance item?
- Did you re-check each finding against the actual diff?
- Did you read the callers of every changed public surface?
- Does every blocker name a consequence, not just a preference?
- Is the verdict explicit — approved, changes requested, or not reviewable?

---

## References

- Matt Pocock, `code-review` skill — https://github.com/mattpocock/skills
- Martin Fowler, *Refactoring* — the smell baseline
- [Section 33](skills/33-pr-change-size-standards.md) — PR size and scope
- [Section 34](skills/34-ai-code-quality-anti-pattern-detection.md) — AI-specific anti-patterns
- [Section 35](skills/35-pr-description-format-template.md) — the description under review
- [Section 68](skills/68-spec-and-ticket-decomposition.md) — the spec to review against
