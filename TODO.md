# TODO.md — Standardized AGENTS.md (Anchor)

## Legend
- ✅ Complete
- 🔄 In Progress
- ⬜ Not Started

## Current Sprint / Phase

| # | Status | Description |
|---|--------|-------------|
| 1 | ✅ | Audit current project state against AGENTS.md |
| 2 | ✅ | Ship the routing map, checkpoints, branch policy, hard stops, and sections 64-66 |
| 3 | ✅ | Ship the local routing/benchmark checker (`scripts/check_structure.py` + `tests/bench_projects.py`) |
| 4 | ✅ | `research/papers/full/` holds the full papers, linked from `research/index.md` |
| 5 | ✅ | Keep `routing.json` and the Section Index in sync — now enforced by `scripts/check_structure.py` |
| 6 | ✅ | Ship sections 67-73 (the delivery loop), the `plan` route, skill frontmatter, and benchmark batch 31 |
| 7 | 🔄 | Ship sections 74-75 (design systems, security audit), design critique, cross-cutting tweaks, and benchmark batch 32 |

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
| 12 | ✅ | Sections 67-73 — elicitation, decomposition, diagnosis, two-axis review, design, domain modeling, retro; `plan` task type |
| 13 | ✅ | Sections 74-75 — design systems and visual craft, security audit loop; 63.7 critique; cross-cutting tweaks; benchmark batch 32 |

## Notes

- Sections 16-20 exist as their own skills: 16 Documentation, 17 Dependencies, 18 Performance, 19 Build/Deployment, 20 External Integrations.
- History lives in `CHANGELOG.md` only. `AGENTS.md` deliberately carries no change log (Section 51).
- Local-only tooling is gitignored: `tests/` (scratch suites + `tests/routing-benchmark.json`), `scripts/`, and `PROJECT.md`.
- Build size delta: N/A (documentation-only project).
- Consumers validate via the structural invariant: every section in the Section Index links to an existing file in `skills/`, and `routing.json` references only sections that exist.
