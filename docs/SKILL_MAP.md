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

Every section is reachable: 66 sections, all loadable by at least one route (core, a task type, a phase, or the router itself). A section no route can load is dead guidance and fails the local check.

## Always loaded

- [1 Core Principles](../skills/01-core-principles.md)
- [2 Commit Protocol](../skills/02-commit-protocol.md)
- [36 Explicit Prohibitions — The "NEVER" List](../skills/36-explicit-prohibitions-the-never-list.md)

Routing itself is [64 Skill Routing & Checkpoints](../skills/64-skill-routing-and-checkpoints.md). Budget: **7** task skills beyond the core.

## Phase boundaries (add / drop)

| Phase | Adds | Drops |
|---|---|---|
| plan | 50, 28 | — |
| build | — | 28 |
| verify | 8, 9, 23, 37, 40 | — |
| commit | 15, 33, 35 | — |

## Task types

| Task type | Triggers | Loads |
|---|---|---|
| **fix** | bug, broken, failing test, error, regression, crash | 34, 10, 24, 25, 27, 14, 3 |
| **feature** | add, build, implement, new endpoint, feature, support for | 35, 12, 17, 24, 62, 63, 5 |
| **refactor** | refactor, rename, extract, split, clean up, simplify | 50, 1, 23, 27, 33, 17, 18 |
| **test** | test, tests, coverage, flaky, property-based, snapshot | 45, 46, 47, 48, 60, 61, 49 |
| **review** | pull request, pr, audit, code quality check, code review, review this | 33, 34, 36, 27, 31, 35, 50 |
| **docs** | docs, readme, changelog, adr, documentation, comments | 16, 4, 6, 39 |
| **release** | release, version, tag, publish, bump, cut a release | 39, 16, 19, 38, 58, 24, 59 |
| **incident** | incident, outage, down, sev, rollback, production is broken | 59, 24, 29, 30, 41, 43 |
| **ui** | ui, frontend, page, component, css, layout | 63, 4, 33, 34, 35, 13, 53 |
| **data** | etl, pipeline, schema, migration, backfill, warehouse | 53, 29, 40, 43, 11, 60, 47 |
| **embedded** | firmware, embedded, microcontroller, mqtt, iot, ota | 53, 7, 20, 30, 41, 62 |
| **infra** | docker, kubernetes, terraform, deploy, container, helm | 32, 30, 38, 41, 42, 47, 7 |
| **security** | security, vulnerability, secret, auth, prompt injection, supply chain | 36, 13, 31, 44, 55, 58, 27 |
| **ai** | agent, llm, rag, mcp, prompt, eval | 53, 54, 55, 56, 57, 24, 21 |
| **deck** | deck, slides, presentation, talk, keynote, pitch | 66, 50, 63 |
| **hackathon** | hackathon, demo, spike, time-boxed, prototype, proof of concept | 65, 6, 36, 63 |
| **cli** | cli, command line, command-line, man page, shell tool, tui | 53, 8, 16, 27, 33, 62 |
| **meta** | agents.md, skill file, skill files, routing map, rule set, ruleset | 51, 22, 24, 26, 50, 52 |

## Notes

- A task type picks the skills; a phase may add and drop at a boundary (plan → build → verify → commit).
- Cross-references inside a skill are real links — load the referenced file rather than guessing its contents.
- The map is data, not logic: the same request always resolves to the same skills.
- Reachability is enforced locally: `python3 scripts/check_structure.py` fails if any section cannot be loaded by some route.
