# Skill 37: Pre-Commit Hook Standards

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 37. Pre-Commit Hook Standards

Pre-commit hooks are a MANDATORY gate, not an optional convenience. They enforce consistency before code ever reaches CI.

### 37.1 Installation — MANDATORY First Step

Before making any changes to a project, run:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

This installs the git hooks and validates the entire existing codebase. If `pre-commit run --all-files` fails, fix the failures before making any other changes.

### 37.2 Standard Configuration Template

Create `.pre-commit-config.yaml` at the project root:

```yaml
repos:
  # --- UNIVERSAL HOOKS (every project) ---

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
        name: Remove trailing whitespace
      - id: end-of-file-fixer
        name: Ensure files end with a newline
      - id: check-yaml
        name: Validate YAML syntax
      - id: check-json
        name: Validate JSON syntax
      - id: check-toml
        name: Validate TOML syntax
      - id: check-added-large-files
        name: Prevent files > 500KB
        args: ['--maxkb=500']
      - id: detect-private-key
        name: Detect accidentally committed private keys
      - id: detect-aws-credentials
        name: Detect accidentally committed AWS credentials
      - id: check-merge-conflict
        name: Check for merge conflict markers
      - id: mixed-line-ending
        name: Normalize line endings
        args: ['--fix=lf']

  # --- PYTHON HOOKS ---

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        name: Lint Python (ruff)
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
        name: Format Python (ruff)

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.0
    hooks:
      - id: mypy
        name: Type check (mypy)
        # Install only the type stubs you actually use — avoid the types-all meta-package
        args: []

  # --- SECURITY HOOKS ---

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.9
    hooks:
      - id: bandit
        name: Security lint (bandit)
        args: [-c, pyproject.toml, --skip=B101]
        # B101: assert — used in tests, skip for production code scan

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.2
    hooks:
      - id: gitleaks
        name: Detect secrets in code

  # --- GENERAL HOOKS ---

  - repo: https://github.com/codespell-project/codespell
    rev: v2.3.0
    hooks:
      - id: codespell
        name: Check spelling
        args: [--write-changes]
```

### 37.3 What Each Hook Catches

| Hook | Catches | Severity if Failed |
|------|---------|--------------------|
| **trailing-whitespace** | Whitespace at end of lines | Low — noisy diffs |
| **end-of-file-fixer** | Missing newline at EOF | Low — POSIX compliance |
| **check-yaml/json/toml** | Malformed config files | HIGH — breaks deployments |
| **check-added-large-files** | Accidental large binary commits | HIGH — bloats repo |
| **detect-private-key** | Committed SSH/PGP keys | CRITICAL — security incident |
| **detect-aws-credentials** | Committed AWS keys | CRITICAL — security incident |
| **check-merge-conflict** | Unresolved `<<<<<<<` markers | HIGH — breaks builds |
| **ruff** | Lint violations | HIGH — code quality |
| **ruff-format** | Format violations | Medium — consistency |
| **mypy** | Type errors | HIGH — runtime bugs |
| **bandit** | Security anti-patterns | HIGH — vulnerabilities |
| **gitleaks** | Any hardcoded secret | CRITICAL — data breach |

### 37.4 Enforcement Policy

- **Pre-commit hooks run on EVERY commit.** If a hook fails, the commit is blocked.
- **CI runs the same hooks** on every push to verify hooks were not skipped.
- **Skipping hooks requires:**
  - Explicit user approval
  - A documented reason in the commit message body (`--no-verify: reason`)
  - The CI will still fail if hooks would have caught the issue
- **Never commit `.pre-commit-config.yaml` changes** that remove hooks without project maintainer approval

### 37.5 CI Verification

```yaml
# In ci.yml, add a pre-commit verification step:
- name: Run pre-commit
  run: pre-commit run --all-files --show-diff-on-failure
```

This catches cases where a developer skipped hooks locally.

### 37.6 Keeping Hooks Current

Pinned revisions rot — schedule `pre-commit autoupdate` (e.g. monthly, or on a dependabot/renovate PR for `.pre-commit-config.yaml`) and review the diff before merging. Prefer widely-maintained hooks: gitleaks (active) over detect-secrets (unmaintained), ruff over the old flake8/pyflakes setup.

### 37.7 Gitleaks Baseline

```bash
# Generate initial baseline (existing secrets are whitelisted)
gitleaks dir --config .gitleaks.toml --report-format sarif --report-path .gitleaks.sarif

# Audit the baseline to ensure no real secrets were whitelisted
# Commit the config so future scans catch NEW secrets only
git add .gitleaks.toml
```

> Gitleaks needs no baseline file to start; any pre-existing secret it flags should be rotated rather than whitelisted.

---

