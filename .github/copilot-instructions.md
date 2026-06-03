# GitHub Copilot Instructions

> All project rules are defined in `AGENTS.md`. Read it before writing any code.

## Required Reading

**Before any task, read these files:**
- `AGENTS.md` — All project rules and conventions
- `DEEPDIVE.md` — System architecture narrative
- `docs/` — Project documentation

## Critical Rules

1. **No dead code** — Remove unused functions, imports, variables immediately
2. **Test-first** — Write tests before code, verify all pass before committing
3. **Full cleanup sweep** before every commit:
   ```bash
   ruff check . && ruff format . && vulture . && mypy .
   ```
4. **tests/ folder** — All tests and random scripts go here; always in `.gitignore`
5. **docs/ and research/** — Create for every new project
6. **Human-sounding commits** — Explain WHY changes were made, not just WHAT changed
7. **DEEPDIVE.md** — Update after any architectural change

## Prohibited Actions

- **NEVER** create PRs, issues, or GitHub activity without explicit user approval
- **NEVER** leave dead code, stubs, or silent exception handlers
- **NEVER** commit without running the full lint/vulture sweep first

## Project Structure

```
project/
├── src/              # Source code
├── tests/            # All tests (gitignored)
├── docs/             # Architecture docs
├── research/         # Research files
├── DEEPDIVE.md       # System narrative
├── AGENTS.md         # This file
└── TODO.md           # Task tracking
```

## Validation Checklist

Before marking any task complete:
- [ ] All tests pass
- [ ] `ruff check .` clean
- [ ] `vulture .` finds no dead code
- [ ] `mypy .` clean (if Python)
- [ ] Human-sounding commit message explaining WHY
- [ ] DEEPDIVE.md updated if architecture changed