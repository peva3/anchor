---
name: skill-16-documentation-requirements
description: "Section 16 — Documentation Requirements. Load when: Writing docs."
---
# Skill 16: Documentation Requirements

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 16. Documentation Requirements

- **README.md** — Setup, quick start, architecture overview
- **API docs** — OpenAPI/Swagger at `/docs` for APIs
- **Architecture docs** — `docs/architecture.md`, ADRs in `docs/adr/`
- **Code comments** — Every non-trivial function needs a docstring explaining WHAT, HOW, WHY
- **AGENTS.md** — This file, updated when project conventions change
- **Research** — See `/research/` folder for AI agent prompt guidance whitepapers

### 16.1 SPEC.md Lives Beside the Code

A module with non-trivial behavior gets a `SPEC.md` at its root, describing the contract
rather than the implementation:

```markdown
# <Module> spec
Purpose: <one sentence>
Inputs / outputs: <shape and meaning>
Invariants: <what must always hold>
Errors: <what can fail and what the caller sees>
Boundaries: <what this module does not do>
Non-goals: <explicitly out of scope>
```

- Write it with the implementation, not after it. A spec reconstructed from the code
  documents the bugs.
- **Change it in the same commit** as a boundary, contract, or decision change. A stale spec
  is worse than no spec because the next agent trusts it.
- Link it from the module README or `AGENTS.md`; do not copy it into `docs/`.
- A small function needs a docstring, not a file. Use judgement, not ceremony.

### 16.2 Documentation Drift Check

Documentation fails by drifting, not by being absent.

- Before commit, list every changed public surface (endpoint, CLI flag, config key, env var,
  exported symbol) and check the document that describes it changed too.
- A drift report compares checked-in docs to source: symbols that no longer exist, endpoints
  missing from the API reference, env vars absent from `.env.example`, commands that fail.
- Make it deterministic where possible — generated API docs, link checks, `--help` snapshots
  ([Section 52](skills/52-rule-enforcement-architecture-from-advisory-to-deterministic.md)).
- State what the check does not cover. "Docs links valid; examples not executed" is honest.


---

