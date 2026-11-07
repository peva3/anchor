---
name: skill-67-requirements-elicitation-grilling
description: "Section 67 — Requirements Elicitation (Grilling). Load when a request is ambiguous, a decision is expensive to reverse, or alignment is needed before building."
---
# Skill 67: Requirements Elicitation (Grilling)

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 67. Requirements Elicitation (Grilling)

Most bad implementations are faithful answers to the wrong question. Grilling is the
structured conversation that turns a vague ask into a decision the user actually owns —
before code is written, not after review.

### 67.1 When to Grill

Grill when at least one is true:

- The request has more than one plausible interpretation.
- The choice is expensive to reverse (schema, public API, auth model, data retention).
- The user described a solution but not the problem.
- Constraints conflict (deadline vs scope, cost vs latency, privacy vs analytics).
- You would have to invent an acceptance criterion to know when you are done.

Do **not** grill a typo fix, a mechanical rename, or a task whose acceptance test is
already unambiguous. Grilling is a cost; spend it where ambiguity is expensive.

### 67.2 Build the Design Tree

Write the decision tree before asking anything. Each node is a decision; each edge is a
dependency between decisions. The **frontier** is the set of decisions whose
prerequisites are already settled — those are the only questions worth asking now.

```
Goal: let customers save a booking
├── Identity: account required, or guest checkout?      ← frontier
│   ├── account → profile storage, password reset
│   └── guest   → email verification, duplicate handling
├── Inventory: hold seats during payment?               ← blocked on identity
└── Notifications: email, SMS, both?                    ← frontier
```

Asking a blocked question produces an answer the user will have to revise. Keep the
frontier visible and work it in rounds.

### 67.3 Ask in Rounds, With a Recommendation

- **Batch the whole frontier into one round.** One message with numbered questions beats
  five turns of interrogation.
- **Every question carries a recommended answer and a one-line reason.** The user can
  accept the default instead of writing an essay.
- **Facts are your job; decisions are the user's.** If the codebase, docs, or a subagent
  can answer it, find it — do not ask. Ask only what changes the design and cannot be
  derived.
- **Name the cost of each option.** "Guest checkout adds duplicate-account handling;
  accounts add a signup step" is a decision aid. "Which do you prefer?" is not.
- **Give 2–4 concrete options, not an open field.** "Postgres, SQLite, or a hosted
  service?" is answerable; "what database do you want?" moves the design work back to the
  user. Include the recommended option and what would change the recommendation.
- **Treat "go ahead" as choosing the recommendation — and say what you inferred.** After a
  blanket approval, list the assumptions you filled in: "Proceeding with: 15-minute holds,
  guest checkout, no admin UI in v1." That gives the user one last cheap place to correct you.

```markdown
1. Should checkout require an account?
   Recommended: guest checkout with optional account creation.
   Why: removes the signup drop-off; the duplicate-account path is bounded.
2. How long should an unpaid hold last?
   Recommended: 15 minutes, configurable.
   Why: matches payment-provider authorization windows.
```

### 67.4 Stop When the Frontier Is Empty

The grill is done when **all** of these hold:

- [ ] Every frontier decision has an answer, or an explicit "you decide" with constraints.
- [ ] You can state the outcome in one sentence without hedging.
- [ ] You can name the acceptance test that proves it.
- [ ] Non-goals are written down, not implied.
- [ ] The user confirms the summary in their own words.

**Play it back in chunks.** Summarize in 3–5 short blocks — goal, decisions, non-goals,
acceptance — and ask for corrections after each. A single 40-line recap gets skimmed and
rubber-stamped; a short block gets read.

If the user says "just build it", record the assumptions you are making, pick the safer
route ([Section 64](skills/64-skill-routing-and-checkpoints.md)), and proceed. Do not
keep asking questions the user has declined to answer.

### 67.5 Write the Brief

The output of grilling is a short written brief, not a transcript. It feeds
[Section 68](skills/68-spec-and-ticket-decomposition.md) and `TODO.md`
([Section 6](skills/06-todo-md-task-tracking-standard.md)).

```markdown
## Goal
One sentence: the outcome, not the implementation.

## Non-goals
What this deliberately does not do.

## Decisions
| Decision | Choice | Why |
|----------|--------|-----|

## Constraints
Deadline, budget, compatibility, compliance, platforms.

## Acceptance
- [ ] Observable behavior that proves the goal
- [ ] Verification command or manual check

## Open questions
Anything still undecided, with an owner and a date.
```

### 67.6 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Interrogation** | Twenty questions with no recommendation pushes the work back to the user | Recommend a default for every question |
| **One question at a time** | Burns turns and hides the shape of the decision tree | Batch the frontier |
| **Asking for facts** | "What database do we use?" is your job to look up | Read the repo; ask only for intent |
| **Silent assumption** | The user discovers the interpretation in the diff | State the assumption and its cost |
| **Faux alignment** | "Does this sound good?" invites a yes without a decision | Ask about the specific trade-off |
| **Grilling a trivial task** | Adds ceremony and latency for no risk | Skip when acceptance is already unambiguous |

### 67.7 Verification

- Did every question change a decision, or was it discoverable?
- Can a new engineer read the brief and know what "done" means?
- Are the non-goals explicit enough to reject scope creep in review?
- Did the user confirm the summary, or did you assume silence was agreement?

---

## References

- Matt Pocock, `grilling` skill — https://github.com/mattpocock/skills
- [Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md) — YAGNI gate before scope grows
- [Section 68](skills/68-spec-and-ticket-decomposition.md) — turn the brief into slices
- [Section 6](skills/06-todo-md-task-tracking-standard.md) — durable task state
