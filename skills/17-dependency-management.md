# Skill 17: Dependency Management

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 17. Dependency Management

- Declare broad version constraints in `pyproject.toml`/`package.json` and commit a **lockfile** (`uv.lock`, `poetry.lock`, `pnpm-lock.yaml`, `package-lock.json`) for reproducible installs — exact-pinning everything blocks security patches
- Run `pip-audit` (PyPA, free) or `npm audit`/`osv-scanner` periodically and in CI to check for vulnerabilities — note `safety` CLI 3.x now requires an account/license, prefer `pip-audit`
- Keep dependencies minimal — avoid adding libraries for simple tasks (see [Section 50.1](skills/50-intentional-minimalism-the-simplicity-first-architecture.md) decision ladder)
- Document why each major dependency exists
- Automate updates (dependabot/renovate) so patches land on a cadence, and review diffs before merging

---

