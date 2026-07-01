# TODO.md — Standardized AGENTS.md (Anchor)

## Legend
- ✅ Complete
- 🔄 In Progress
- ⬜ Not Started

## Current Sprint / Phase

| # | Status | Description |
|---|--------|-------------|
| 1 | ✅ | Audit current project state against AGENTS.md |
| 2 | 🔄 | Fix the gaps found in audit |
| 3 | ⬜ | Add CI workflow that runs the audit on every push |
| 4 | ⬜ | Add pre-commit hooks and make audit a local hook |
| 5 | ⬜ | Sync all 7 platform config files to mention Sections 33, 37, 50.1, 50.2 |
| 6 | ⬜ | Add instruction-provenance tags to AGENTS.md sections per 51.5 |
| 7 | ⬜ | Decide and execute first tagged release (v1.0.0) |
| 8 | ⬜ | Populate or remove empty `research/papers/full/` directory |

## Completed Sprints

| Sprint | Status | Deliverable |
|--------|--------|-------------|
| 1 | ✅ | Sections 1-26 covering core, git, security, testing, AI guidance |
| 2 | ✅ | Sections 27-32 covering code quality, tech stack, ops, health, security, Docker |
| 3 | ✅ | Sections 33-36 covering PR standards, anti-patterns, templates, NEVER list |
| 4 | ✅ | Sections 37-41 covering pre-commit, CI/CD, semver, coverage, observability |
| 5 | ✅ | Sections 42-44 covering IaC, backups, secrets |
| 6 | ✅ | Sections 45-49 covering flaky tests, mutation, benchmarks, contracts, chaos |
| 7 | ✅ | Section 50 — Intentional Minimalism (decision ladder) |
| 8 | ✅ | Section 51 — Instruction Architecture (lazy loading, context budgets) |
| 9 | ✅ | Rebrand to "Anchor" with SEO-optimized README |
| 10 | ✅ | Add Section 36 financial/identity NEVER rules |
| 11 | ✅ | Repo self-audit identified 33 issues; fixes in flight |

## Notes

- Sections 16-20 (Documentation, Dependencies, Performance, Build/Deployment, External Integrations) are referenced in the AGENTS.md change log and audit but were merged into adjacent sections in the rewrite. See Section 16 for documentation, Section 17 for dependencies, Section 18 for performance, Section 19 for build, Section 20 for external integrations.
- Build size delta: N/A (documentation-only project).
- The audit script (`tests/test_agents_md_quality.py`) is the source of truth for the section count and line count. Re-run it before tagging a release.
