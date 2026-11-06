---
name: skill-71-codebase-design-deep-modules
description: "Section 71 — Codebase Design. Load when shaping modules, interfaces, seams, or refactoring boundaries."
---
# Skill 71: Codebase Design

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 71. Codebase Design

Good design is not "more abstraction". It is **leverage**: a small interface that hides a
large amount of behavior, placed at a seam where it can be tested and replaced.

### 71.1 Vocabulary

| Term | Meaning | Use it to ask |
|------|---------|---------------|
| **Module** | A unit with an interface and an implementation | What does this hide? |
| **Interface** | Everything a caller must know: types, errors, ordering, invariants | Is this the smallest honest contract? |
| **Implementation** | The code behind the interface | Can I change it without touching callers? |
| **Depth** | Behavior delivered per unit of interface | Is the interface small relative to what it does? |
| **Seam** | A place where behavior can be substituted without editing the caller | Can a test replace this? |
| **Adapter** | A concrete implementation of an interface at a seam | Is there a second implementation yet? |
| **Leverage** | How much behavior one interface unlocks | Does this abstraction pay for itself? |
| **Locality** | Related change stays in one place | Does one change touch five files? |

### 71.2 Deep Modules

A **deep module** has a small interface and a lot inside. A **shallow module** has an
interface nearly as complex as its implementation — it adds a layer without hiding anything.

```
Deep:   parse(source) -> AST          # one call, lexer/parser/errors hidden
Shallow: parse_lex(), parse_expr(), parse_stmt(), parse_error()  # caller orchestrates
```

**The deletion test:** if deleting the module makes the callers no worse, it was not hiding
anything. Delete it ([Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md)).

**The interface is the test surface.** Test through the interface, not the implementation.
If a test must reach inside, the interface is missing a capability or the seam is wrong.

### 71.3 Seams

- A seam is where you can change behavior **without editing the caller**. Dependency
  injection, a module boundary, a port, or a function parameter all create seams.
- **One adapter is a hypothetical seam; two are a real seam.** Do not build an abstraction
  for a single implementation "in case" — add it when the second case arrives
  ([Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md)).
- Put the seam at the **external boundary** you do not control: clock, network, filesystem,
  payment provider, model API. Those are the places tests need to substitute.
- A seam that exists only for tests and has no production second implementation is still
  useful when the dependency is non-deterministic; name it as a test seam.

### 71.4 Dependencies and Results

- **Accept dependencies, return results.** Pass the clock, client, or repository in; return
  a value. Do not read globals, call `now()` deep inside, or write to a singleton.
- **Errors are part of the interface.** Decide whether the module raises, returns a result
  type, or logs and degrades — and document it ([Section 10](skills/10-error-handling-patterns.md)).
- **Ordering and idempotency are interface contracts.** If callers must call `init()` first,
  or retries must be safe, say so at the interface.
- Depend in one direction. A cycle is two modules that should be one, or a missing seam.

### 71.5 Refactor Moves

| Move | When | Check |
|------|------|-------|
| **Extract module** | A file has several reasons to change | Callers use the new interface |
| **Hide implementation** | Callers reach into internals | Nothing outside imports the internals |
| **Collapse shallow wrapper** | A layer only delegates | Deletion test passes |
| **Move seam to the boundary** | Tests need to fake a deep dependency | One adapter in prod, one in tests |
| **Split by reason to change** | Divergent change | Each module changes for one reason |
| **Inline a one-use helper** | A helper has one caller and no name value | The caller reads better |

Refactors are behavior-preserving. Run the suite after each move
([Section 23](skills/23-verification-gates.md)); a wide move uses
expand → migrate → contract ([Section 68](skills/68-spec-and-ticket-decomposition.md)).

### 71.6 Review Questions

- What does this module hide from its callers?
- Is the interface smaller than the implementation, or merely a pass-through?
- Where is the seam, and can a test substitute the non-deterministic part?
- Does adding a second implementation require editing callers?
- Is the dependency direction one-way, and are errors part of the contract?
- Would deleting this module make the codebase simpler with no loss?

### 71.7 Anti-Patterns

| Anti-pattern | Why it fails | Do instead |
|--------------|--------------|------------|
| **Abstraction for one case** | Speculative generality | Wait for the second implementation |
| **Shallow wrapper** | Adds a layer, hides nothing | Collapse or deepen it |
| **Leaky interface** | Callers depend on internals | Hide the representation |
| **Hidden clock/network** | Tests are flaky and slow | Inject at the seam |
| **God module** | Every change touches it | Split by reason to change |
| **Cycle** | Changes cascade both ways | Merge or introduce a seam |

### 71.8 Verification

- Can you name what each new module hides?
- Does every seam have a production and a test adapter, or a documented reason?
- Do callers compile without knowledge of the implementation?
- Is the suite green after each refactor move?

---

## References

- Matt Pocock, `codebase-design` skill — https://github.com/mattpocock/skills
- Michael Feathers, *Working Effectively with Legacy Code* — seams
- John Ousterhout, *A Philosophy of Software Design* — deep modules
- [Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md) — YAGNI and the deletion test
- [Section 68](skills/68-spec-and-ticket-decomposition.md) — slicing wide refactors
