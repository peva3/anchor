---
name: skill-73-retrospective
description: "Section 73 — Retrospective. Load after a sprint, incident, repeated correction, or benchmark run to turn evidence into one durable improvement."
---
# Skill 73: Retrospective

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 73. Retrospective

A retro is not a feelings meeting. It is a short, evidence-based loop that turns a failure
or a repeated correction into **one** durable change — preferably a check, not a paragraph.

### 73.1 When to Run One

- A sprint or milestone closes.
- An incident is resolved ([Section 59](skills/59-incident-response-and-runbooks.md)).
- The user corrected the same behavior more than once.
- A benchmark regressed, or a rule was ignored twice.
- A task took materially longer than its slice suggested.

Skip it when there is no evidence and no repeated failure; a retro with nothing to inspect
becomes ceremony.

### 73.2 Gather Evidence First

| Evidence | Question it answers |
|----------|---------------------|
| Diffs and commits | What actually changed, and how large was it? |
| Test and benchmark output | Did quality move, or just activity? |
| Routing traces | Which skills loaded, which should have? |
| User corrections | Where did the instructions fail? |
| Incident timeline | What was the detection and recovery path? |
| TODO.md history | What slipped, and why? |

No evidence, no finding. "It felt slow" is a prompt to measure, not a conclusion.

### 73.3 Categories

| Category | Look for |
|----------|----------|
| **Navigation** | Wrong route, missing trigger, skill loaded too late |
| **Automated checks** | A bug a linter/test could have caught |
| **Coding standards** | A rule that exists but was not followed |
| **Global instructions** | A missing or contradictory rule in `AGENTS.md` |
| **Tool economy** | Context spent on skills the task did not need |
| **No-ops** | Instructions that changed nothing observable |
| **Information access** | Facts that took too many files to find |

### 73.4 Fix the Mechanism, Not the Person

Rank remedies by durability:

1. **Deterministic check** — a test, lint rule, schema, or pre-commit hook. Cannot be
   forgotten.
2. **Template or scaffold** — the correct path is the easy path.
3. **Prose rule in `AGENTS.md`** — necessary for judgement, but easy to skip under pressure.
4. **Exhortation** — "be more careful". The weakest option; avoid it.

A rule that can be checked mechanically should be checked mechanically
([Section 52](skills/52-rule-enforcement-architecture-from-advisory-to-deterministic.md)).
A prose rule is for judgement that cannot be encoded.

### 73.5 The Output Is One Change

```markdown
## Retro — <date / sprint / incident>

**What happened:** one paragraph, factual.
**Why:** the mechanism, not the person.
**Change:** the single durable fix (check > template > prose).
**Owner:** who lands it.
**Verification:** the command or test that proves it works.
**Follow-up:** anything deliberately deferred, with a date.
```

One retro, one change. A list of ten resolutions is a wish list; nothing lands.

### 73.6 Agent-Specific Questions

- Did the route match the work, or did the task change type mid-flight?
- Which loaded skill was never used? Why was it loaded?
- Which rule was missed because it lived in a skill that was not loaded?
- Did context pressure cause a shortcut?
- Is there a duplicate or contradictory rule between `AGENTS.md` and a skill?
- Did a benchmark case exist for this failure? If not, add one.

### 73.7 Close the Loop

- [ ] The change is filed in `TODO.md` ([Section 6](skills/06-todo-md-task-tracking-standard.md)).
- [ ] A test or benchmark case reproduces the failure
      ([Section 8](skills/08-testing-requirements.md)).
- [ ] The rule, if prose, is in exactly one place and cross-referenced.
- [ ] The changelog records the behavior change ([Section 39](skills/39-semantic-versioning-changelog.md)).
- [ ] The next retro checks whether the change held.

### 73.8 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Blame** | Hides the mechanism | Fix the system, not the person |
| **Vibes-only** | No evidence, no learning | Measure first |
| **Ten action items** | None land | One durable change |
| **Prose-only fix** | Forgotten under pressure | Prefer a deterministic check |
| **Retro with no follow-up** | Same failure recurs | File it and verify next time |
| **Rewriting history** | Loses the signal | Record what happened, then change the rule |

### 73.9 Verification

- Is every finding backed by a diff, log, benchmark, or correction?
- Is the chosen fix the most durable option available?
- Is there exactly one change, with an owner and a verification?
- Will the next run detect a recurrence?

---

## References

- Matt Pocock, `retro` skill — https://github.com/mattpocock/skills
- [Section 51.2](skills/51-instruction-architecture-context-economy-self-improvement.md) — self-maintaining instructions
- [Section 52](skills/52-rule-enforcement-architecture-from-advisory-to-deterministic.md) — checks over prose
- [Section 64.9](skills/64-skill-routing-and-checkpoints.md) — vocabulary gaps
- [Section 6](skills/06-todo-md-task-tracking-standard.md) — durable follow-up
