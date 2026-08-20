# Skill 09: Linting & Type Checking

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 9. Linting & Type Checking

**Before EVERY commit, run a full cleanup sweep:**

```bash
ruff check .                  # Lint
ruff format .                 # Format
ruff check --select=E,F,W     # Explicit errors/warnings
vulture .                     # Find dead code (uncalled functions)
mypy .                        # Type check (if available)
```

**The sweep must prove:**
- No unused imports, variables, or functions
- No functions that are defined but never called
- No dead-end code paths (code with no return/raise at end)
- No type errors
- No lint errors

**If vulture reports any findings:**
- Delete the unused code immediately
- If you're unsure whether code is truly dead, search for all references with `grep -r "function_name" .`
- Only keep code that has a proven production call path

**Do not commit until the sweep is clean.**

---

