# GitHub Copilot Instructions

> All project rules are defined in `AGENTS.md`. Read it before writing any code.

## Required Reading

**Before any task, read these files:**
- `AGENTS.md` — All project rules and conventions
- `DEEPDIVE.md` — System architecture narrative
- `docs/` — Project documentation

## Critical Rules

1. **No dead code** — Remove unused functions, imports, variables immediately (Section 1)
2. **Test-first** — Write tests before code, verify all pass before committing (Section 8)
3. **Full cleanup sweep** before every commit:
   ```bash
   ruff check . && ruff format . && vulture . && mypy .
   ```
4. **tests/ folder** — All tests and random scripts go here; always in `.gitignore` (Section 5)
5. **docs/ and research/** — Create for every new project (Section 5)
6. **Human-sounding commits** — Explain WHY changes were made, not just WHAT changed (Section 15)
7. **DEEPDIVE.md** — Update after any architectural change (Section 5)
8. **PR size limit** — 800 lines max, 500 for complex logic (Section 33)
9. **Decision ladder** — YAGNI → stdlib → native → existing dep → one line → minimum (Section 50.1)
10. **Tradeoff comments** — Name the ceiling and upgrade trigger for any intentional shortcut (Section 50.2)
11. **Pre-commit hooks mandatory** — Install and run before every commit (Section 37)

## Prohibited Actions

- **NEVER** create PRs, issues, or GitHub activity without explicit user approval (Section 2)
- **NEVER** leave dead code, stubs, or silent exception handlers (Section 1)
- **NEVER** commit without running the full lint/vulture sweep first (Section 9)
- **NEVER** skip pre-commit hooks (Section 37)
- **NEVER** submit a PR over 800 lines (Section 33)

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
- [ ] PR under 800 lines, single feature (Section 33)
- [ ] Pre-commit hooks passed (Section 37)
- [ ] Tradeoff comments added for any shortcuts (Section 50.2)
- [ ] Decision ladder applied (Section 50.1)
