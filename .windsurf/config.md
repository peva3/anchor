# Windsurf AI Configuration

> Project-level rules for Windsurf Code agent. See `AGENTS.md` for complete guidelines.

## How to Use

1. Read `AGENTS.md` before starting any work
2. Read `DEEPDIVE.md` for system architecture context
3. Follow all rules in AGENTS.md — they apply to every file and every task

## Pre-Commit Validation

Run before every commit:
```
ruff check . && ruff format . && vulture . && mypy .
```

Clean = commit. Dirty = fix first.

## Required Project Structure

```
project/
├── src/           # Source code
├── tests/         # Tests + random scripts (gitignored)
├── docs/          # Documentation
├── research/      # Research files
├── DEEPDIVE.md    # System narrative (update on architecture changes)
├── AGENTS.md      # Project rules (this file references it)
└── TODO.md        # Task tracking
```

## Critical Rules

| Rule | Description |
|------|-------------|
| No dead code | Remove unused functions/imports immediately |
| Test-first | Write tests before code |
| Human commits | WHY-focused, not "fix: bug" |
| Auto-push | After validation, if gh works, push |
| Never rogue | No GitHub activity without user approval |
| Update DEEPDIVE | After any architectural change |

## Prohibited Actions

- Creating PRs, issues, comments without explicit user approval
- Leaving dead code or unused imports
- Committing without lint/vulture sweep passing
- Skipping tests or validation