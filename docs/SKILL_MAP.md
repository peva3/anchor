# Skill Map

How the rules are organised and which ones a task loads. Generated from [`routing.json`](../routing.json) — if the two disagree, the JSON is right.

## The shape of the ruleset

```
AGENTS.md (always loaded, ~400 lines)
├── Sections 1, 2, 36      core rules — inline, apply to every task
├── Section Index          every section, its trigger, and its file
└── routing.json           task type → skills to load

skills/ (66 files, lazy-loaded)
└── NN-name.md             full text of one section
```

## Always loaded

- [1 Core Principles](../skills/01-core-principles.md)
- [2 Commit Protocol](../skills/02-commit-protocol.md)
- [36 Explicit Prohibitions — The "NEVER" List](../skills/36-explicit-prohibitions-the-never-list.md)

Routing itself is [64 Skill Routing & Checkpoints](../skills/64-skill-routing-and-checkpoints.md). Active-skill budget: **7**.

## Loading at phase boundaries

| Phase | Adds |
|---|---|
| plan | 50 |
| build | — |
| verify | 8, 23, 40 |
| commit | 15, 33, 35 |

## Task types

| Task type | Triggers | Loads |
|---|---|---|
| **fix** | bug, broken, failing test, error, regression, crash | 34, 10, 24, 25, 27, 40, 45 |
| **feature** | add, build, implement, new endpoint, feature, support for | 35, 5, 8, 12, 16, 27, 40 |
| **refactor** | refactor, rename, extract, split, clean up, simplify | 50, 1, 23, 27, 33, 40 |
| **test** | test, tests, coverage, flaky, property-based, snapshot | 27, 45, 46, 47, 48, 60, 61 |
| **review** | review, pull request, pr, audit, code quality check | 33, 34, 36, 27, 31, 35, 50 |
| **docs** | docs, readme, changelog, adr, documentation, comments | 16, 4, 6, 39 |
| **release** | release, version, tag, publish, bump, cut a release | 39, 16, 19, 38, 58 |
| **incident** | incident, outage, down, sev, rollback, production is broken | 59, 24, 29, 30, 41, 43 |
| **ui** | ui, frontend, page, component, css, layout | 63, 4, 33, 34, 35 |
| **data** | etl, pipeline, schema, migration, backfill, warehouse | 53, 29, 40, 42, 43 |
| **infra** | docker, kubernetes, terraform, deploy, container, helm | 32, 7, 19, 30, 38, 41, 42 |
| **security** | security, vulnerability, secret, auth, prompt injection, supply chain | 36, 13, 31, 44, 54, 55, 58 |
| **ai** | agent, llm, rag, mcp, prompt, eval | 53, 31, 54, 55, 56, 57, 58 |
| **deck** | deck, slides, presentation, talk, keynote, pitch | 66, 50, 63 |
| **hackathon** | hackathon, demo, spike, time-boxed, prototype, proof of concept | 65, 6, 36, 63 |

## Notes

- A task type picks the skills; a phase may add more at a boundary (plan → build → verify → commit).
- Cross-references inside a skill are real links — load the referenced file rather than guessing its contents.
- The map is data, not logic: the same request always resolves to the same skills.
- To check it locally: `python3 scripts/check_structure.py` (every referenced skill exists, no task type exceeds the budget).
