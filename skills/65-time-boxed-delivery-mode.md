# Skill 65: Time-Boxed Delivery Mode

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 65. Time-Boxed Delivery Mode

Hackathons, demos, and spike weeks are legitimate. They are not permission to lower the bar everywhere — they are permission to *narrow where the bar applies*. This skill defines that narrowing so a fast build does not quietly become a shipped liability.

### 65.1 The Demo Path Gets Full Rigor

Identify the **demo path** first: the exact sequence a person will click, call, or run on stage. That path gets production treatment, no exceptions.

| Demo path element | Required |
|-------------------|----------|
| Every control the demo touches | Real behavior — no dead buttons, no unlabeled placeholders ([Section 63](skills/63-ui-quality-and-anti-slop-guardrails.md)) |
| Every value shown on screen | Real or explicitly labeled illustrative ([Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md) 50.6) |
| The happy path | Tested end-to-end, by you, before the demo |
| Any secret or key the demo uses | Scoped, rotated, never committed ([Section 44](skills/44-secrets-management.md)) |
| Any exposed endpoint | Authenticated, or explicitly temporary and taken down after |

Everything outside the demo path moves fast — that is the point of the mode.

### 65.2 Mark Every Shortcut

A shortcut without a marker is a shortcut nobody cleans up. Every deliberate shortcut gets a searchable marker in the code:

```python
# HACKATHON: hardcoded fixture data — replace with repository query before any real use
```

Rules for markers:

- One marker per shortcut, at the exact place the shortcut lives
- State **what** is fake and **what** the real version must do
- Never mark a bright-line violation (see 65.4) — those are not shortcuts, they are defects
- Do not mark the same shortcut in five places and call it five tasks

### 65.3 Turn Markers Into a Cleanup List

Before the work is considered finished — and always before it merges to the default branch — collect them:

```bash
grep -rn "HACKATHON:" --include="*.py" --include="*.ts" --include="*.tsx" .
```

Each hit becomes a row in `TODO.md` ([Section 6](skills/06-todo-md-task-tracking-standard.md)) with an owner and a target. The grep also clears the markers once addressed, so the list cannot silently rot.

### 65.4 Bright Lines Never Relax

Time pressure is the most common reason rules get broken, so these stay absolute regardless of clock:

- The NEVER list ([Section 36](skills/36-explicit-prohibitions-the-never-list.md)) — all of it
- Committing `.env`, keys, tokens, or credentials ([Section 36](skills/36-explicit-prohibitions-the-never-list.md) 36.2)
- Fabricated testimonials, users, metrics, or compliance claims ([Section 63](skills/63-ui-quality-and-anti-slop-guardrails.md) 63.1)
- "We'll add tests later" on the demo path — the demo path is tested now
- Disabling authentication, TLS verification, or permission checks to save time
- Attributing work to anyone but the configured identity ([Section 2](skills/02-commit-protocol.md))

If a deadline cannot be met without breaking one of these, the correct move is to cut scope and say so — not to cut the line.

### 65.5 Exit Criteria

The mode ends when the clock does, not when the code is "good enough." Before declaring the time-boxed work done or mergeable:

- [ ] Demo path verified end-to-end
- [ ] Every `HACKATHON:` marker triaged into `TODO.md` (or removed because it was fixed)
- [ ] No bright-line rule (65.4) was traded away
- [ ] Anything temporarily exposed is taken down or explicitly scheduled for takedown
- [ ] The next reader can tell what is real and what is a stub, without asking you

---

## References

- [Section 6](skills/06-todo-md-task-tracking-standard.md) — TODO.md cleanup list
- [Section 36](skills/36-explicit-prohibitions-the-never-list.md) — bright lines
- [Section 63](skills/63-ui-quality-and-anti-slop-guardrails.md) — no fabricated content, no dead controls
