# Skill 36: Explicit Prohibitions — The "NEVER" List

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 36. Explicit Prohibitions — The "NEVER" List

This section exists because general guidelines are too easy to rationalize around. These are bright lines.

### 36.1 Code NEVER

- **NEVER** use mutable default arguments (`def f(x=[])`) — use `None` + create new, or `field(default_factory=...)`
- **NEVER** use bare `except:` — always catch specific exception types
- **NEVER** use `except Exception: pass` — silent failure is forbidden. If truly non-critical, comment WHY
- **NEVER** use `eval()`, `exec()`, or `compile()` on any user-supplied input
- **NEVER** use string interpolation for SQL queries — always parameterized queries
- **NEVER** use `os.system()` or `subprocess` with `shell=True` and untrusted input
- **NEVER** import within functions to avoid circular imports — restructure the modules instead (exception: `TYPE_CHECKING` imports)
- **NEVER** create small helper methods that are referenced only once — inline the logic
- **NEVER** add `bool` or ambiguous `Optional` parameters that force callers to write `foo(False)` or `bar(None)` — use keyword-only arguments or separate methods

### 36.2 Git NEVER

- **NEVER** force push to shared branches (`main`, `develop`, any branch others might be using)
- **NEVER** commit `.env` files, credentials, API keys, or secrets of any kind
- **NEVER** `git add .` — add specific files by name, verify with `git diff --cached`
- **NEVER** amend commits that have already been pushed
- **NEVER** skip hooks (`--no-verify`, `--no-gpg-sign`) unless you have explicit permission and a documented reason
- **NEVER** push directly to `main` or `master` — always use a feature branch and PR

### 36.3 GitHub NEVER

- **NEVER** create a PR without explicit user approval (per Section 2 "Never Go Rogue" rule)
- **NEVER** comment on issues/PRs without explicit user approval
- **NEVER** close issues or PRs that you did not open
- **NEVER** assign reviewers or request changes without user direction
- **NEVER** merge a PR without explicit user approval

### 36.4 Financial NEVER

- **NEVER** create GitHub Actions workflows that use paid runners, consume API credits, or incur any financial cost without explicit user confirmation
- **NEVER** enable GitHub features that trigger billing — large runners, Packages beyond free tier, Codespaces beyond free limits, Copilot for business, Advanced Security, etc.
- **NEVER** sign up for paid cloud services, provision resources with billing attached, or register for API keys tied to a credit card
- **NEVER** modify billing settings, change plan tiers, enable paid add-ons, or accept terms that involve financial commitment
- **NEVER** create CI/CD workflows that call paid third-party APIs (e.g., paid SaaS monitoring, commercial testing services, paid deployment platforms) without explicit confirmation
- **NEVER** purchase domains, SSL certificates, or any infrastructure that costs money
- When in doubt — if any action involves an external service that could possibly charge money — **ask the user first**

### 36.4a GitHub Automation NEVER (no Actions, no bot PRs)

This subsection is broader than 36.4 (financial) and exists because the user owns the maintainer relationship with GitHub, not the agent. Even free-tier automation costs the user reviewer time, runs without their supervision, and creates artifacts (workflow runs, PRs, branches) that they must clean up.

- **NEVER** create GitHub Actions workflow files (anything under `.github/workflows/*.yml` or `.github/workflows/*.yaml`) without explicit, per-workflow user approval. "It's just CI" is not approval.
- **NEVER** create GitHub-side automation that opens pull requests or issues on the user's behalf (`dependabot.yml`, `renovate.json`, scheduled workflows, `gh-actions` cron triggers) without explicit user approval.
- **NEVER** enable GitHub repository settings that trigger work the user has not requested (branch protection rules that auto-delete, required status checks that point at workflows the user did not approve, auto-merge rules, etc.) without explicit user approval.
- **NEVER** add GitHub Apps, OAuth integrations, or third-party CI providers (Codecov, Snyk, CodeClimate, etc.) without explicit user approval — these commonly have paid tiers that auto-upgrade.
- **NEVER** assume "free tier" means zero cost. Free Actions still cost minutes, storage, and the user's review queue. If the workflow runs on every PR, multiply by the PR cadence.
- **DO** propose GitHub Actions as a recommendation when the user asks for CI, but wait for explicit approval before writing the file.
- **DO** ship the audit script and pre-commit hooks (Section 37) — these run locally and need no GitHub-side automation.
- **DO** ship PR/issue templates and CODEOWNERS — these are static markdown, not automation, and don't trigger Actions.
- When in doubt — if a change touches `.github/workflows/`, `dependabot.yml`, `renovate.json`, or any repository setting that auto-runs something — **ask the user first**.

### 36.5 Identity NEVER

- **NEVER** impersonate another user, use a different GitHub username, or create a separate bot account for any activity
- **NEVER** sign commits, create PRs, post comments, or author any content under an identity other than the configured author
- **NEVER** attribute work to "the AI" or "the agent" in commit messages, PR descriptions, issue comments, or documentation — all work is authored by and attributed to the human user
- **NEVER** claim the agent acted independently — the user directs the agent, the user authors all output
- **NEVER** configure git with a different username or email than what is already set globally
- **NEVER** use an AI-generated signature, bot handle, or fake persona in any user-facing communication

### 36.6 Testing NEVER

- **NEVER** merge code that has failing tests
- **NEVER** skip tests because "the change is small" — small changes cause big bugs
- **NEVER** write tests that depend on execution order — every test must be independently runnable
- **NEVER** write tests with `time.sleep()` to wait for async operations — use proper synchronization
- **NEVER** write tests that pass vacuously (no assertions, or assertions that can never fail)
- **NEVER** mark a task complete without running the full test suite

### 36.7 Documentation NEVER

- **NEVER** add general product or user-facing documentation to the `docs/` folder when using an LLM to generate it — docs should be human-curated
- **NEVER** leave DEEPDIVE.md stale after an architectural change — update it as part of the change
- **NEVER** comment self-evident operations — `# Increment counter by 1` above `counter += 1`
- **NEVER** write docstrings that restate the function signature — explain WHY, not WHAT

### 36.6 AI Agent NEVER

- **NEVER** guess when you can verify — run the code, check the logs, read the actual file
- **NEVER** assume a library is available — check `pyproject.toml` or `requirements.txt` first
- **NEVER** add a dependency without checking if an existing dependency already provides that functionality
- **NEVER** modify generated code (OpenAPI clients, protobuf stubs, migration files) — regenerate instead
- **NEVER** skip linting/type-checking before committing — Section 9 sweep is mandatory
- **NEVER** submit code you haven't tested — run the test suite, verify the behavior

---

