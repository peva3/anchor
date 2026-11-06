---
name: skill-68-spec-and-ticket-decomposition
description: "Section 68 — Spec & Ticket Decomposition. Load when turning an agreed outcome into a written spec, vertical slices, or a ticket graph."
---
# Skill 68: Spec & Ticket Decomposition

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 68. Spec & Ticket Decomposition

A spec is a contract about **what** will be true when the work is done. Tickets are the
smallest independently demoable steps that get there. Both exist to keep a long task
inside one fresh context window at a time.

### 68.1 The Spec Shape

Write the spec before the tickets. Keep it to one page unless the change is genuinely
cross-cutting.

| Section | Must answer | Failure if missing |
|---------|-------------|--------------------|
| **Problem** | What is broken or missing, for whom? | The work optimizes the wrong thing |
| **Outcome** | What is observably true afterward? | "Done" is a matter of opinion |
| **Non-goals** | What is explicitly out of scope? | Scope creep survives review |
| **Constraints** | Compatibility, data, latency, budget, deadline | A correct design that cannot ship |
| **Acceptance** | The checks that prove the outcome | Tests test the implementation, not the requirement |
| **Risks** | What could break, and the rollback | Surprises land in production |
| **Open questions** | Undecided items with an owner | Silent assumptions become defects |

The spec restates the **problem and the contract**, not the request. If it reads like the
user's message with headings added, it is not a spec yet.

### 68.2 Slice Vertically, Not Horizontally

A **vertical slice** (tracer bullet) touches every layer needed to deliver one observable
behavior: schema, code, test, and wiring. It is demoable on its own.

```
Horizontal (wrong)                 Vertical (right)
├── all migrations                 ├── slice 1: create + read one booking
├── all repositories               ├── slice 2: list + paginate bookings
├── all services                   ├── slice 3: cancel + refund
└── all endpoints                  └── slice 4: notifications
```

Horizontal slicing produces branches that cannot be tested until the last layer lands.
Vertical slicing produces a working system after the first slice and keeps every slice
releasable ([Section 33](skills/33-pr-change-size-standards.md)).

**Slice rules:**

- **One behavior per slice.** "Create a booking" is a slice; "the booking module" is not.
- **Demoable alone.** If it needs the next slice to be visible, merge the two.
- **Sized to one fresh context window.** If you cannot hold the slice's files and tests in
  one sitting, split it.
- **Blocking edges are explicit.** A slice that cannot start until another lands says so.
- **Every slice carries its tests.** A slice with tests deferred is half a slice.

### 68.3 The Ticket Template

```markdown
## <Verb> <observable outcome>

**Why:** the user-visible problem this closes.
**Scope:** the files or boundaries this may touch.
**Out of scope:** what this deliberately leaves alone.

**Acceptance**
- [ ] Behavior that can be observed or queried
- [ ] Test that fails before and passes after
- [ ] Verification command

**Depends on:** #ticket or "none"
**Size:** S / M / L (L must be split)
**Risk:** low / medium / high — and the rollback for high
```

A ticket without an acceptance check is a wish. A ticket without a size is a schedule
risk. A ticket with no "out of scope" is a scope-creep invitation.

### 68.4 Size and Dependency

- **S** — one file or one small module, one test, under an hour.
- **M** — a few files across one boundary, half a day.
- **L** — crosses more than one boundary or needs a migration; split before starting.
- **XL** — not a ticket; it is a project. Return to [Section 67](skills/67-requirements-elicitation-grilling.md).

Order the graph so **blocking edges point forward**: foundations first, but each slice
still delivers behavior. Do not create a "phase 0" that produces no observable change
unless it is a genuine prerequisite (a migration, a feature flag, a contract).

### 68.5 Wide Refactors Are the Exception

A behavior-preserving refactor that touches every call site cannot be sliced by behavior.
Use **expand → migrate → contract**:

1. **Expand** — add the new path beside the old one; both work.
2. **Migrate** — move call sites in batches, keeping the suite green after each batch.
3. **Contract** — delete the old path once nothing calls it.

Each batch is a ticket. The correctness check is the existing suite, not a new behavior
([Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md),
[Section 33](skills/33-pr-change-size-standards.md)).

### 68.6 Quiz the User on Granularity

Before filing, show the slice list and ask two questions:

1. **Is any slice too big to review in one sitting?**
2. **Is any dependency edge wrong, or missing?**

The user owns the granularity because they own the review load. Adjust before work
starts, not after three branches are open.

### 68.7 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Spec restates the request** | Adds ceremony, no shared understanding | State problem, outcome, non-goals |
| **Tickets by layer** | Nothing is demoable until the end | Slice by observable behavior |
| **Giant ticket** | Review and rollback become all-or-nothing | Split into S/M slices |
| **No acceptance test** | "Done" is unverifiable | One test that fails first |
| **Hidden dependency** | Parallel work collides at merge | Draw the blocking edges |
| **Spec after code** | Rationalizes what was built | Spec before the first slice |

### 68.8 Verification

- Does every ticket name an observable outcome and a verification command?
- Can the first slice ship alone without breaking the suite?
- Is every "L" split, and every "XL" sent back to grilling?
- Do the non-goals match the brief from [Section 67](skills/67-requirements-elicitation-grilling.md)?
- Is the ticket graph recorded in `TODO.md` ([Section 6](skills/06-todo-md-task-tracking-standard.md))?

---

## References

- Matt Pocock, `to-tickets` and `tdd` skills — https://github.com/mattpocock/skills
- [Section 67](skills/67-requirements-elicitation-grilling.md) — the brief this decomposes
- [Section 6](skills/06-todo-md-task-tracking-standard.md) — where the graph lives
- [Section 33](skills/33-pr-change-size-standards.md) — size limits per change
- [Section 70](skills/70-two-axis-code-review.md) — review against this spec
