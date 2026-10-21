# Skill Map

How the rules are organised and which ones a task loads. Generated from [`routing.json`](../routing.json) — if the two disagree, the JSON is right.

## The shape of the ruleset

```
AGENTS.md (always loaded, ~408 lines)
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

Routing itself is [64 Skill Routing & Checkpoints](../skills/64-skill-routing-and-checkpoints.md). Budget: **8 task skills** beyond the core.

## Phase boundaries

| Phase | Adds | Drops |
|---|---|---|
| plan | 50, 28 | — |
| build | — | 28 |
| verify | 8, 9, 23, 37, 40 | — |
| commit | 15, 33, 35 | all domain skills |

> The commit phase keeps only the core plus the git/PR rules: a commit is a write-up, not a build. That is what holds commit-time context near 44% of a 32K window instead of 86%.

## Task types

| Task type | Loads |
|---|---|
| **fix** | 34, 10, 24, 25, 27, 14, 3 |
| **feature** | 35, 27, 12, 17, 24, 62, 63 |
| **refactor** | 50, 1, 23, 27, 33, 17, 18, 5 |
| **test** | 45, 46, 47, 8, 60, 61, 49 |
| **review** | 33, 34, 36, 27, 31, 35, 50 |
| **docs** | 16, 4, 6, 39 |
| **release** | 39, 16, 19, 38, 58, 24, 59 |
| **incident** | 59, 24, 29, 30, 41, 43 |
| **ui** | 63, 4, 33, 34, 35, 13, 53 |
| **data** | 53, 29, 40, 43, 11, 60, 47 |
| **embedded** | 53, 7, 20, 30, 41, 62 |
| **integration** | 20, 12, 13, 24, 41, 48, 62 |
| **infra** | 32, 30, 38, 41, 42, 47, 7 |
| **security** | 36, 13, 31, 44, 55, 58, 27 |
| **ai** | 53, 54, 55, 56, 57, 24, 21 |
| **deck** | 66, 50, 63 |
| **hackathon** | 65, 6, 36, 63 |
| **cli** | 53, 8, 16, 27, 33, 62 |
| **meta** | 51, 22, 24, 26, 50, 52 |

## Notes

- A task type picks the skills; phases add at boundaries and drop what no longer applies.
- Cross-references inside a skill are real links — load the referenced file rather than guessing.
- One owner per trigger phrase, whole-word matching, and a fallback is a reported gap (Section 64.9).
- Check locally: `python3 scripts/check_structure.py` (links, reachability, vocabulary hygiene, core↔skill drift).
