# CLAUDE.desktop.md — Claude Desktop App Instructions

> Loaded automatically when this repo is opened in the Claude desktop app.

## Required Reading

**You MUST read these files before working:**
1. `AGENTS.md` — All project rules and conventions (mandatory)
2. `DEEPDIVE.md` — System architecture and design decisions

## Critical Rules from AGENTS.md

### Before Any Commit
```bash
ruff check . && ruff format . && vulture . && mypy .
```

### Required Folders
- `tests/` — All tests + random scripts (always gitignored)
- `docs/` — Architecture documentation
- `research/` — Whitepapers, references

### Commit Style
Explain WHY changes were made, not just WHAT changed.
Bad: "fix bug"
Good: "Prevented race condition in token refresh by adding mutex"

### Prohibited
- NO PRs, issues, or GitHub activity without explicit user approval
- NO dead code or unused imports
- NO commits without passing full lint/vulture sweep

## Architecture Context

See DEEPDIVE.md for detailed system narrative including:
- Why the project is structured this way
- Key architectural decisions and trade-offs
- Known failure modes and gotchas

## Questions?

If anything is unclear, ask the user for clarification before proceeding.