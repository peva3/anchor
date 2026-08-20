# Skill 25: Common Gotchas

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 25. Common Gotchas

Lessons learned from multiple projects — things that regularly bite developers.

### 25.1 Python Version Mismatches
- Ensure Python 3.12+ for modern projects
- Use `python3 -m venv` to specify version explicitly
- Check with `python --version` before installing packages

### 25.2 Shell Command Failures
- Remember `snip` prepends to all commands automatically
- Use `bash -c '...'` format for built-ins (`cd`, `export`, `source`)
- Direct `cd` commands will fail

### 25.3 Environment Variables
- Always create `.env` from `.env.example`
- Never commit `.env` (it's in `.gitignore`)
- Missing env vars cause silent failures — check logs

### 25.4 Package Conflicts
- Use fresh virtual environments
- Install from lockfiles, not individual packages
- Run `pip freeze` to see exact versions installed

### 25.5 Type Errors
- Run `mypy` before committing
- Don't use `Any` — use `unknown` if type is truly unknown
- Generic types need explicit parameters: `list[str]` not `list`

### 25.6 Import Order
- Ruff auto-fixes import order: `ruff check --fix .`
- Stdlib → third-party → local, alphabetical within groups
- Run format check before committing

### 25.7 Race Conditions
- Concurrent operations on shared state need locks
- Test concurrent access explicitly
- Log when acquiring/releasing locks for debugging

### 25.8 Testing edge cases
- Test the empty case (empty list, empty string, None)
- Test the overflow case (very large input)
- Test the concurrent case (multiple simultaneous calls)

### 25.9 Git Mistakes
- Never `git add .` — add specific files
- Check `git diff --cached` before committing
- Use `git status` to verify what will be pushed

### 25.10 Docker Debugging
- Use `docker compose logs <service>` to see what's failing
- `docker compose exec <service> bash` to get shell inside
- Restart with `docker compose restart <service>`

---

