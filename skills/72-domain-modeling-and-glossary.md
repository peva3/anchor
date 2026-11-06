---
name: skill-72-domain-modeling-and-glossary
description: "Section 72 — Domain Modeling & Glossary. Load when defining domain terms, invariants, a GLOSSARY.md, or an ADR."
---
# Skill 72: Domain Modeling & Glossary

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 72. Domain Modeling & Glossary

Code drifts from the business when the same word means three things. A glossary and a
small set of architecture decision records keep the **language** and the **why** stable
while the implementation changes.

### 72.1 The Ubiquitous Language

One term, one meaning, everywhere — code, tests, docs, and conversation.

`GLOSSARY.md` at the repo root:

```markdown
# Glossary

## Booking
A reservation of a resource for a time range, before payment is captured.
Code: `Booking` (`src/bookings/model.py`).
Not: an order, a payment, or a calendar event.

## Hold
A temporary reservation that expires. A hold is not a booking.
Code: `Hold`; expires after `HOLD_TTL`.
```

**Rules:**

- **One canonical term per concept.** List the rejected synonyms ("do not call it an order").
- **Name the code symbol.** A glossary that does not map to code is a dictionary, not a model.
- **Define by behavior, not by data.** What it means, what it guarantees, what it is not.
- **Update it in the same PR** that renames or splits a concept.
- **Keep it short.** Every term must earn its line; a glossary nobody reads is sediment.

### 72.2 Model the Domain, Not the Screen

- **Entities** have identity and a lifecycle (`Booking` changes state; its ID is stable).
- **Value objects** are defined by their values (`Money`, `DateRange`, `Email`); they are
  immutable and validate on construction.
- **Invariants** are rules that must hold at every boundary: a booking cannot overlap
  itself, money is integer minor units, a hold cannot outlive its TTL.
- **State transitions** are explicit: `held → confirmed → cancelled`; anything else is a bug.

Do not let the database schema or the UI form define the model. Both are representations;
the domain rules live in one place ([Section 71](skills/71-codebase-design-deep-modules.md)).

### 72.3 Architecture Decision Records

An ADR captures a decision **and the alternatives**, so the next engineer does not relitigate
it from scratch.

```markdown
# ADR-0007: Store money as integer minor units

- Status: accepted
- Date: 2026-11-06
- Deciders: payments team

## Context
Floating-point arithmetic produced rounding drift in ledger reconciliation.

## Decision
All amounts are integers in the currency's minor unit, with an explicit currency code.
Rounding happens once, at the presentation boundary.

## Consequences
- Positive: exact sums, deterministic tests.
- Negative: every input must convert; the conversion is a boundary concern.
- Rejected: `Decimal` everywhere (heavier, easy to mix with floats).

## Links
Section 72, `src/money.py`, ADR-0004.
```

**ADR rules:**

- **Number sequentially, never reuse.** `docs/adr/0007-...md`.
- **Immutable once accepted.** Supersede with a new ADR; do not rewrite history.
- **Record the rejected options.** The "why not" is the value.
- **Keep it under a page.** Context, decision, consequences, links.
- **Write one when the choice is expensive to reverse**, not for every small change.

### 72.4 When to Add a Term or an ADR

| Signal | Add |
|--------|-----|
| Two people use the same word for different things | Glossary entry with the rejected synonym |
| A rule is enforced in code but written nowhere | Invariant in the glossary or domain doc |
| A choice will be questioned in six months | ADR with alternatives |
| A migration changes a core concept | ADR + glossary update in the same PR |
| A new team member needs a day to learn a term | Glossary entry |

Do **not** add an ADR for a reversible implementation detail; that is a code comment or a
PR note ([Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md)).

### 72.5 Where It Lives

- `GLOSSARY.md` at the repo root, linked from `AGENTS.md` and `README.md`.
- `docs/adr/NNNN-title.md`, one decision per file.
- Domain docs beside the code when the codebase is a monorepo; link, do not duplicate.
- The glossary is **not** a second README. It defines terms; it does not explain setup.

### 72.6 Maintenance

- Review glossary and ADRs when a PR renames a concept or changes an invariant.
- Delete a term that no longer exists in code; a stale glossary teaches the wrong language.
- Cross-link the ADR from the code it governs (one line, not a paragraph).
- Run a link check in CI or pre-commit ([Section 37](skills/37-pre-commit-hook-standards.md)).

### 72.7 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Glossary of data fields** | Restates the schema | Define behavior and meaning |
| **Synonym soup** | Every team uses a different word | One canonical term, rejected synonyms listed |
| **ADR as a novel** | Nobody reads it | One page: context, decision, consequences |
| **Rewriting accepted ADRs** | Erases the reasoning | Supersede with a new ADR |
| **Glossary with no code link** | Drifts immediately | Name the symbol and file |
| **ADR for every PR** | Ceremony without value | Only expensive-to-reverse choices |

### 72.8 Verification

- Does every core term have one definition and a code symbol?
- Are invariants stated where a new contributor will find them?
- Does each ADR record the alternatives and consequences?
- Did the PR update the glossary/ADR when it changed the domain?
- Are all links to `GLOSSARY.md` and ADRs valid?

---

## References

- Eric Evans, *Domain-Driven Design* — ubiquitous language
- Michael Nygard, "Documenting Architecture Decisions"
- [Section 16](skills/16-documentation-requirements.md) — documentation standards
- [Section 71](skills/71-codebase-design-deep-modules.md) — module boundaries
