# Skill 52: Rule Enforcement Architecture — From Advisory to Deterministic

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 52. Rule Enforcement Architecture — From Advisory to Deterministic

AGENTS.md alone is the **soft layer** — the model reads prose and hopefully follows it. But hope is not a strategy. The industry is converging on a **two-layer enforcement model**: advisory rules (what we have) PLUS deterministic enforcement (what we need to add to every project).

### 52.1 The Two-Layer Model

```
LAYER 1 (Soft) — Advisory / Prompt Injection
  AGENTS.md, CLAUDE.md, copilot-instructions, .cursorrules
  ──→ Model reads rules as context, attempts to follow them.
      PRO: Flexible, covers any rule.
      CON: No guarantee. Model can ignore, forget, or override.

LAYER 2 (Hard) — Deterministic / Hooks & Validation
  PreToolUse hooks, permission deny rules, pre-commit hooks, CI gates
  ──→ Code enforces rules. Model cannot override.
      PRO: 100% compliance for covered rules.
      CON: Only covers rules expressible as code.
```

**Rules that MUST have hard-layer enforcement:**
- Preventing destructive operations (`rm -rf`, `git push --force`)
- Protecting sensitive files (.env, secrets, credentials)
- Blocking force push to protected branches
- Preventing commits without tests passing
- Blocking changes that exceed PR size limits
- Preventing code that doesn't compile/parse

**Rules that can remain soft-layer:**
- Code style preferences
- Documentation quality expectations
- Commit message format conventions
- Architecture pattern preferences

### 52.2 Compiling Prose Rules Into Hooks

The most powerful new pattern: parse your AGENTS.md prose rules and generate actual hook code that enforces them at runtime.

**Pattern: Rule → Hook Compilation**

```json
// hooks/enforce-pr-size.json — compiled from AGENTS.md Section 33.1
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash(git push*)",
      "hooks": [{
        "type": "command",
        "command": "hooks/check-pr-size.sh",
        "description": "Block push if PR exceeds 800 lines"
      }]
    }]
  }
}
```

```bash
# hooks/check-pr-size.sh — prevents pushing oversized PRs
CHANGES=$(git diff --stat origin/main | tail -1 | awk '{print $1}')
if [ "$CHANGES" -gt 800 ]; then
  echo "BLOCKED: PR size $CHANGES lines exceeds 800-line limit (AGENTS.md Section 33.1)"
  exit 2  # Exit code 2 blocks the action
fi
```

**Hook compilation checklist — every project should compile THESE rules from AGENTS.md to hooks:**

| AGENTS.md Rule | Hook Type | Triggers On | Blocks When |
|---------------|-----------|-------------|-------------|
| Section 2: Never go rogue | Permission deny | `gh pr create`, `gh issue create` | No explicit approval |
| Section 33.1: PR size limit | PreToolUse(Bash) | `git push` | Diff exceeds 800 lines |
| Section 36.2: No force push | PreToolUse(Bash) | `git push --force` | Always (exit code 2) |
| Section 9: Lint before commit | PreToolUse(Bash) | `git commit` | `ruff check .` fails |
| Section 40: Coverage floor | CI job | `pull_request` | Coverage drops below 80% |
| Section 13: No secrets in code | Git hook | `git commit` | `detect-secrets` finds a secret |
| Section 36.4: No paid services | PreToolUse(WebFetch) | Any API domain | Domain matches known paid service |
| Section 44: Encrypted secrets | Git hook + CI | `git commit` + PR | Unencrypted secret detected |

### 52.3 Pre-commit Hooks as Deterministic Gate

Pre-commit hooks (Section 37) are the most universal hard-layer enforcement — they work with ANY agent, not just ones that support hook systems.

**Minimum hard-layer hooks every project must have:**

```yaml
# .pre-commit-config.yaml — compiled from AGENTS.md rules
repos:
  # Section 13: No secrets in code
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        name: "BLOCK: secrets in code (AGENTS.md S13)"

  # Section 9: No dead code before commit
  - repo: local
    hooks:
      - id: vulture-check
        name: "BLOCK: dead code detected (AGENTS.md S9)"
        entry: vulture .
        language: system
        types: [python]

  # Section 33.1: PR size limit
      - id: pr-size-check
        name: "BLOCK: changes exceed 800 lines (AGENTS.md S33.1)"
        entry: bash -c 'git diff --cached --stat | tail -1 | awk "{if (\$1+0 > 800) exit 1}"'
        language: system
        pass_filenames: false

  # Section 36.2: No force push
      - id: no-force-push
        name: "BLOCK: force push prohibited (AGENTS.md S36.2)"
        entry: bash -c 'if echo "$PRE_COMMIT_REMOTE_BRANCH" | grep -q "+"; then echo "Force push blocked"; exit 1; fi'
        language: system
        pass_filenames: false
        stages: [pre-push]

  # Section 36.4: No paid GitHub Actions
      - id: no-large-runners
        name: "BLOCK: paid runner detected (AGENTS.md S36.4)"
        entry: bash -c 'grep -r "runs-on:.*large\|runs-on:.*gpu" .github/workflows/ && exit 1 || exit 0'
        language: system
        pass_filenames: false
```

### 52.4 Runtime Hook Architecture (Claude Code / Codex)

For agents that support hooks, compile AGENTS.md rules into JSON hook definitions:

```json
// .claude/settings.json — hard-layer enforcement
{
  "permissions": {
    "deny": [
      "Bash(git push --force *)",           // Section 36.2
      "Bash(rm -rf /*)",                     // Section 36.1
      "Bash(git config user.*)",             // Section 2 (identity)
      "WebFetch(domain:openai.com/api*)",    // Free-tier only unless approved
      "WebFetch(domain:anthropic.com/api*)"  // Free-tier only unless approved
    ],
    "allow": [
      "Read(*.md)",
      "Read(*.py)",
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(pytest*)",
      "Bash(ruff*)",
      "Bash(mypy*)",
      "Bash(vulture*)"
    ],
    "ask": [
      "Bash(pip install *)",
      "Bash(npm install *)",
      "WebFetch(*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "hooks/pr-size-guard.sh",
            "description": "AGENTS.md S33.1: Block push if PR > 800 lines"
          }
        ]
      },
      {
        "matcher": "Bash(git commit *)",
        "hooks": [
          {
            "type": "command",
            "command": "hooks/lint-guard.sh",
            "description": "AGENTS.md S9: Block commit if lint fails"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "description": "AGENTS.md S23: Run test suite before agent can stop. Only exit if tests pass.",
            "prompt": "Run 'pytest --cov=. --cov-fail-under=80' and report results. If tests fail, the agent must NOT stop."
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "hooks/vulture-sweep.sh",
            "description": "AGENTS.md S9: Check for dead code after every edit"
          }
        ]
      }
    ]
  }
}
```

### 52.5 Evidence-First Methodology

The soft layer's biggest weakness is that rules can be read, understood, and then **silently ignored**. The countermeasure: require evidence for every claim.

**Core principle:** Every assertion about code, behavior, or the project must cite a `file:line` reference. No unsupported claims.

```
# Standard format for evidence citations:
file_path:start_line-end_line — brief description

# Examples:
src/api/routes.py:42-58 — the POST /users endpoint validates input with Pydantic
tests/test_api.py:103 — test_post_user_invalid_email_returns_422 covers this case
AGENTS.md:33.1 — PR size limit is 800 lines
```

**When to use evidence citations:**
- Claiming something is implemented → cite the file and line
- Claiming something is tested → cite the test file and line
- Claiming a convention exists → cite the AGENTS.md section
- Claiming a function has no callers → show the vulture output as evidence
- Claiming tests pass → show the actual test output, not "they should pass"

**When evidence IS required:**
- All bug reports ("X is broken")
- All feature claims ("X is implemented")
- All refactoring justifications ("X is dead code because...")
- All security claims ("X is safe because...")

**When evidence is NOT required:**
- Future plans ("we should add X")
- Opinions ("X would be cleaner")
- Standard knowledge ("Python is interpreted")

### 52.6 Rule Verification — Testing That Rules Are Followed

You can test whether agents actually follow the rules in AGENTS.md. This is the meta-test: test the tests.

**Pattern: Behavioral rule compliance test**

```python
# tests/compliance/test_rule_enforcement.py
"""Verify that AGENTS.md rules are actually followed."""

import subprocess
from pathlib import Path

def test_no_dead_code_in_commits():
    """Section 1, 9: No commit should introduce dead code."""
    result = subprocess.run(
        ["vulture", "."],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Dead code found:\n{result.stdout}"

def test_pr_size_under_800_lines():
    """Section 33.1: Current diff must not exceed 800 lines."""
    result = subprocess.run(
        ["git", "diff", "--stat", "origin/main"],
        capture_output=True,
        text=True
    )
    line = result.stdout.strip().split("\n")[-1]
    if "changed" in line:
        changes = int(line.split()[0])
        assert changes <= 800, f"PR size {changes} lines exceeds 800-line limit"

def test_no_secrets_in_repo():
    """Section 13, 44: No secrets committed to repository."""
    result = subprocess.run(
        ["detect-secrets", "scan", "--all-files"],
        capture_output=True,
        text=True
    )
    assert "RESULTS:" not in result.stdout, f"Secrets found:\n{result.stdout}"

def test_ci_workflow_exists():
    """Section 38: CI pipeline must be configured."""
    workflows = list(Path(".github/workflows").glob("*.yml"))
    assert len(workflows) > 0, "No CI workflows found in .github/workflows/"

def test_pre_commit_config_exists():
    """Section 37: Pre-commit hooks must be configured."""
    assert Path(".pre-commit-config.yaml").exists(), \
        "No .pre-commit-config.yaml found — pre-commit hooks not configured"

def test_coverage_above_threshold():
    """Section 40: Coverage must be at or above 80%."""
    result = subprocess.run(
        ["pytest", "--cov=.", "--cov-report=term-missing", "--cov-fail-under=80"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Coverage below 80%:\n{result.stdout[-500:]}"
```

**When to run compliance tests:**
- In CI — every PR triggers compliance checks
- Weekly — full compliance audit via cron
- Pre-commit — fast checks (secrets, dead code) run before every commit

### 52.7 Structured Rule Formats — Beyond Free-Text Markdown

Free-text prose rules have two fatal problems for enforcement:
1. An automated system cannot reliably parse "don't do X" from prose
2. The same rule phrased differently means different things to different models

**Pattern: Rule with structured detection metadata**

```yaml
# .ai-rules/no-force-push.md — structured format for deterministic compilation
---
rule_id: NO_FORCE_PUSH
severity: critical
source: AGENTS.md Section 36.2
description: Never force push to shared branches
enforcement:
  type: pre_push_hook
  detection:
    pattern: "git push.*--force|git push.*\\+[a-z]+/main"
    on_match: block
  human_readable: |
    Force pushing rewrites remote history and can destroy
    collaborators' work. Always use `git push` without --force
    on shared branches.
evidence_id: NO_FORCE_PUSH_001
---
```

**Benefits of structured rules:**
- Automated tools can COMPILE the rule into a hook
- The `detection` pattern is machine-readable — works across agents
- `severity` enables graduated response (warn vs block vs CI-fail)
- `source` provides traceability back to AGENTS.md
- `evidence_id` enables automated compliance reporting

### 52.8 CI-Based Rule Enforcement Gates

The final layer: CI jobs that verify AGENTS.md compliance and block merges.

```yaml
# .github/workflows/rule-compliance.yml
# Compiles AGENTS.md rules into CI checks
name: Rule Compliance Audit

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly full audit

jobs:
  rule-checks:
    name: AGENTS.md Rule Compliance
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

      - name: S9 - No dead code
        run: |
          pip install vulture
          vulture . --min-confidence 80

      - name: S13 - No secrets in code
        run: |
          pip install detect-secrets
          detect-secrets scan --all-files

      - name: S23 - Verification gate checklist
        run: |
          # Check all checklist items in Section 23.4
          grep -q "All functions have production call paths" AGENTS.md
          echo "Verification checklist present"

      - name: S33.1 - PR size gate
        run: |
          CHANGES=$(git diff --stat origin/main | tail -1 | awk '{print $1}')
          if [ "$CHANGES" -gt 800 ]; then
            echo "FAIL: PR has $CHANGES lines, exceeds 800-line max (AGENTS.md S33.1)"
            exit 1
          fi
          echo "PR size: $CHANGES lines (within 800-line limit)"

      - name: S37 - Pre-commit config present
        run: |
          test -f .pre-commit-config.yaml || (echo "FAIL: No pre-commit config (AGENTS.md S37)" && exit 1)

      - name: S38 - CI workflow present
        run: |
          test -n "$(ls .github/workflows/ci*.yml 2>/dev/null)" || (echo "FAIL: No CI workflow (AGENTS.md S38)" && exit 1)

      - name: S40 - Coverage gate
        run: |
          pip install pytest-cov
          pytest --cov=. --cov-fail-under=80 --cov-report=term || (echo "FAIL: Coverage below 80% (AGENTS.md S40)" && exit 1)

      - name: S44 - Check .env is in gitignore
        run: |
          grep -q "^\.env$" .gitignore || (echo "FAIL: .env not in gitignore (AGENTS.md S44)" && exit 1)

      - name: Generate compliance report
        if: always()
        run: |
          echo "## AGENTS.md Compliance Report" >> $GITHUB_STEP_SUMMARY
          echo "| Rule | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|------|--------|" >> $GITHUB_STEP_SUMMARY
          # Parse job results to populate
```

### 52.9 Hook Compilation Quick Reference

| AGENTS.md Section | Hook Type | Implementation | Priority |
|------------------|-----------|---------------|----------|
| 2 (Never rogue) | Permission deny | Block `gh pr create`, `gh issue create` | CRITICAL |
| 2 (Never spend) | Permission deny + pre-commit | Block paid runner YAML + API domain access | CRITICAL |
| 2 (Use user identity) | Permission deny | Block `git config user.*` changes | CRITICAL |
| 9 (Lint before commit) | PreToolUse(Bash) | `ruff check .` exit code gates commit | HIGH |
| 13 (No secrets) | Git hook + CI | `detect-secrets` on pre-commit + CI | CRITICAL |
| 33.1 (PR size) | PreToolUse(Bash) + CI | `git diff --stat` gate at 800 lines | HIGH |
| 36.2 (No force push) | Permission deny | Block `git push --force` to main | CRITICAL |
| 36.3 (No rogue GitHub) | Permission deny | Block `gh pr/issue` unless approved | HIGH |
| 36.4 (No paid services) | Permission deny + pre-commit | Block `runs-on.*large\|gpu` + API domains | CRITICAL |
| 37 (Pre-commit installed) | CI check | Assert `.pre-commit-config.yaml` exists | HIGH |
| 38 (CI workflow) | CI check | Assert `.github/workflows/ci*.yml` exists | HIGH |
| 40 (Coverage floor) | CI check | `--cov-fail-under=80` in CI | HIGH |
| 44 (No committed secrets) | Git hook + CI | `detect-secrets` + `gitleaks` | CRITICAL |
| 23 (Verification gates) | Stop hook (agent) | Run tests + lint, block exit on failure | MEDIUM |

---

---

