# Skill 38: CI/CD Pipeline Standards

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 38. CI/CD Pipeline Standards

**Section 36.4a is in effect:** do not create any of the GitHub Actions workflows in this section without explicit, per-workflow user approval. The templates below are reference material — present them as a recommendation when the user asks for CI, but wait for approval before writing the file.

The pre-commit hook (Section 37) and the audit script (`tests/test_agents_md_quality.py`) run locally and need no GitHub-side automation.

### 38.1 CI Pipeline — `.github/workflows/ci.yml`

Runs on every push to any branch and every PR to main.

```yaml
name: CI

on:
  push:
    branches: ['**']
  pull_request:
    branches: [main, master]

jobs:
  lint-and-typecheck:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b # v5.3.0
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: pip install ruff mypy
      - name: Ruff lint
        run: ruff check .
      - name: Ruff format check
        run: ruff format --check .
      - name: Mypy type check
        run: mypy . --ignore-missing-imports

  test:
    name: Tests (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    needs: lint-and-typecheck
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b # v5.3.0
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      - name: Run tests
        run: pytest --cov=. --cov-fail-under=80 --cov-report=xml --cov-report=term-missing --junitxml=test-results.xml
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
      - name: Upload coverage to Codecov
        if: success() || failure()
        uses: codecov/codecov-action@b9fd7d16f6d7d1b1d2a1d8e5f6b3c4d9e0a1b2c3 # v4.6.0
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  build:
    name: Build (if applicable)
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - name: Build Docker image
        run: docker build -t app:${{ github.sha }} .
      - name: Verify image runs
        run: docker run --rm app:${{ github.sha }} python -c "print('OK')"

  pre-commit:
    name: Pre-commit hooks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
      - uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b # v5.3.0
        with:
          python-version: '3.12'
      - run: pip install pre-commit
      - run: pre-commit run --all-files --show-diff-on-failure
```

### 38.2 Release Pipeline — `.github/workflows/release.yml`

```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

      - name: Extract changelog
        id: changelog
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          # Extract the section for this version from CHANGELOG.md
          CHANGES=$(awk "/## \[${VERSION}\]/{flag=1; next} /## \[/{flag=0} flag" CHANGELOG.md)
          echo "changes<<EOF" >> $GITHUB_OUTPUT
          echo "$CHANGES" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Build artifacts
        run: |
          pip install build
          python -m build

      - name: Create GitHub Release
        uses: softprops/action-gh-release@c062e08bd53281541eafdbcacf16d7f6566b254f # v2.1.0
        with:
          body: ${{ steps.changelog.outputs.changes }}
          files: dist/*
          generate_release_notes: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 38.3 Deployment Pipeline — `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  workflow_run:
    workflows: [CI]
    types: [completed]
    branches: [main]

jobs:
  deploy-staging:
    name: Deploy to Staging
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

      - name: Build and push Docker image
        run: |
          docker build -t registry.example.com/app:${GITHUB_SHA} .
          docker push registry.example.com/app:${GITHUB_SHA}

      - name: Deploy to staging
        run: |
          # Deploy command depends on infrastructure
          echo "Deploying ${GITHUB_SHA} to staging..."

      - name: Verify deployment
        run: |
          # Smoke test the deployed service
          sleep 10
          curl -f http://staging.example.com/health

      - name: Notify on failure
        if: failure()
        run: |
          echo "Deployment to staging failed for commit ${GITHUB_SHA}"

  deploy-production:
    name: Deploy to Production
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Production deployment requires manual approval"
      # Production deployments should be triggered manually or via release
```

### 38.4 GitHub Actions SHA-Pinning Convention

**CRITICAL:** All third-party GitHub Actions MUST be pinned to a full 40-character commit SHA:

```yaml
# CORRECT — pinned to SHA with version comment
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

# WRONG — mutable tag, could be hijacked
uses: actions/checkout@v4
uses: actions/checkout@main
```

- **Exception:** GitHub-authored actions (`actions/*`, `github/*`) are exempt from SHA-pinning
- **Every third-party action** (community or vendor) MUST use full SHA
- **The version tag comment** (`# v4.2.2`) is REQUIRED for human readability and audit
- **Update SHAs** when upgrading action versions — never leave a stale SHA

### 38.5 PR and Issue Templates

Create these files in `.github/`:

**`.github/PULL_REQUEST_TEMPLATE.md`:**
```markdown
<!-- See AGENTS.md Section 35 for the full PR template -->

## Description
### What Changed
### Why
### How
### Testing
- [ ] Unit tests pass
- [ ] Integration tests pass

### Breaking Changes

## AI Agent Disclosure
### Agent Decision Log
### Areas Needing Human Review
### Agent Self-Check
- [ ] Code follows project conventions
- [ ] No dead code (vulture clean)
- [ ] No unused imports (ruff clean)
- [ ] Type check passes (mypy clean)
- [ ] Tests cover new behavior
- [ ] Change size is within limits (under 800 lines)
```

**`.github/ISSUE_TEMPLATE/bug_report.md`:**
```markdown
---
name: Bug Report
about: Report a bug or unexpected behavior
title: 'bug: '
labels: ['bug']
assignees: []
---

### Description
<Clear, concise description of the bug>

### Steps to Reproduce
1.
2.
3.

### Expected Behavior
<What should have happened>

### Actual Behavior
<What actually happened, including error messages>

### Environment
- OS:
- Python version:
- Project version:
```

### 38.6 Branch Protection Rules

Configure these in GitHub repository settings → Branches → Branch protection rules:

| Rule | Value | Rationale |
|------|-------|-----------|
| **Require PR before merging** | Enabled | No direct pushes to main |
| **Require approvals** | 1 minimum | At least one reviewer |
| **Dismiss stale reviews** | Enabled | Re-review after new commits |
| **Require status checks** | Enabled | CI must pass before merge |
| **Required checks** | lint, test, build, pre-commit | All CI jobs must pass |
| **Require branches to be up to date** | Enabled | Must merge main into branch first |
| **Require conversation resolution** | Enabled | All review threads resolved |
| **Require linear history** | Disabled (team preference) | Squash merges handle this |
| **Do not allow bypass** | Enabled for admins too | No one bypasses protection |

---

