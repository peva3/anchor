# Continue.dev Configuration

> Config for Continue.dev AI assistant. See `AGENTS.md` for full rules.

## Workspace Rules

1. **AGENTS.md is mandatory** — Read before any task
2. **DEEPDIVE.md** — Read for system architecture context
3. Follow all project conventions in AGENTS.md

## Pre-Commit Checklist

```bash
ruff check .          # Lint
ruff format .         # Format
vulture .             # Dead code detection
mypy .                # Type checking
```

All must pass before committing.

## Project Structure Requirements

- `tests/` — All tests and random scripts (always gitignored)
- `docs/` — Required for every project
- `research/` — Required for every project
- `DEEPDIVE.md` — Living system narrative, update on architecture changes

## Commit Guidelines

Human-sounding commit messages that explain WHY:
```
<type>: <what changed>

<problem>: Why this needed fixing
<solution>: What the change does and why
<context>: Decisions, trade-offs, gotchas
```

## Prohibited

- GitHub PRs/issues without explicit user approval
- Dead code or unused imports
- Skipping lint/vulture sweep
- Skipping tests

## Quick Reference

| Command | Purpose |
|---------|---------|
| `ruff check .` | Lint check |
| `ruff format .` | Format code |
| `vulture .` | Find dead code |
| `mypy .` | Type check |