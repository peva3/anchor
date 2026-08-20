# Skill 40: Code Coverage Enforcement

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 40. Code Coverage Enforcement

Coverage is a necessary but insufficient quality metric. It tells you what code is NOT tested, not whether the tests are good.

### 40.1 Coverage Thresholds — Hard Enforcement

| Scope | Threshold | Enforcement |
|-------|-----------|-------------|
| **Project overall** | 80% line coverage | CI fails if below (`--cov-fail-under=80`) |
| **Critical paths** | 95%+ | Auth, payment, data mutation — manual review required |
| **New code** | 90%+ | New functions should not reduce overall coverage |
| **Branch coverage** | 75%+ | Measures if both sides of every branch are tested |

### 40.2 CI Configuration

```yaml
# In ci.yml test job:
- name: Run tests with coverage
  run: |
    pytest \
      --cov=. \
      --cov-fail-under=80 \
      --cov-report=xml:coverage.xml \
      --cov-report=term-missing \
      --cov-report=html:coverage-html \
      --junitxml=test-results.xml \
      tests/
```

### 40.3 Coverage Configuration — `.coveragerc` or `pyproject.toml`

```toml
# pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__init__.py",
    "src/main.py",               # Entrypoint, hard to unit test
    "src/core/config.py",        # Pure config, tested implicitly
]

[tool.coverage.report]
show_missing = true
skip_covered = false
fail_under = 80

[tool.coverage.html]
directory = "coverage-html"

# Lines to exclude from coverage
exclude_also = [
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
    "pragma: no cover",
]
```

### 40.4 Excluding Code from Coverage

```python
# Use for code that genuinely cannot be tested:
def _debug_only_function():  # pragma: no cover
    """Used only during development debugging."""
    ...

# Use for platform-specific code:
if sys.platform == "win32":  # pragma: no cover
    def platform_specific():
        ...

# NEVER use 'no cover' to avoid writing tests
# NEVER use 'no cover' because "it's hard to test"
# ONLY use 'no cover' when testing is truly impossible (debug tools, platform guards)
```

### 40.5 Branch Coverage — Why It Matters

Line coverage is deceptive. This function has 100% line coverage but 50% branch coverage:

```python
def divide(a: int, b: int) -> float | None:
    if b == 0:                    # Branch: True or False
        return None               # Only tested with b=0
    return a / b                  # Only tested with b!=0
```

To get 100% branch coverage, you need tests for both `b == 0` and `b != 0`.

**Enable branch coverage:**
```bash
pytest --cov=. --cov-branch --cov-report=term-missing
```

### 40.6 What Coverage Cannot Tell You

Coverage does NOT measure:
- **Test quality** — A test with no assertions has 100% coverage but zero value
- **Edge case coverage** — Tests might call functions but not exercise boundary conditions
- **Integration correctness** — Unit tests with 100% coverage can still miss integration bugs
- **Behavioral correctness** — Covered code can still produce wrong results

**Therefore:** Coverage is a floor, not a ceiling. Meeting the threshold is the minimum. Good tests are the goal.

---

