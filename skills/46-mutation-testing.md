# Skill 46: Mutation Testing

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 46. Mutation Testing

Line/branch coverage tells you what code EXECUTES — mutation testing tells you what code is actually TESTED (tested meaning: tests fail when code behavior changes).

### 46.1 What Mutation Testing Does

Mutation testing introduces small bugs ("mutants") into your code and checks if your tests catch them:

```python
# Original code
def is_adult(age: int) -> bool:
    return age >= 18

# Mutant 1: Relational operator replacement
def is_adult(age: int) -> bool:
    return age > 18  # Changed >= to > — test should catch this

# Mutant 2: Constant replacement
def is_adult(age: int) -> bool:
    return age >= 0  # Changed 18 to 0 — test should catch this

# Mutant 3: Statement deletion
def is_adult(age: int) -> bool:
    pass  # Entire body removed — test should catch this
```

If your tests PASS for any mutant, that mutant "survived" — meaning the code is not properly tested. The goal is to kill >95% of mutants.

### 46.2 Setup with mutmut

```bash
# Install mutmut
pip install mutmut

# Run mutation testing
mutmut run --paths-to-mutate=src/

# Show results
mutmut results

# Show surviving mutants
mutmut show

# Apply surviving mutants to source (for inspection)
mutmut apply <mutant_id>
```

### 46.3 CI Integration

```yaml
# In CI — run on main branch or weekly
mutation-test:
  name: Mutation Testing
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
  strategy:
    matrix:
      python-version: ['3.12']
  steps:
    - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
    - uses: actions/setup-python@0b93645e9fea7318ecaed2b359559ac225c90a2b # v5.3.0
      with:
        python-version: ${{ matrix.python-version }}
    - run: pip install -r requirements.txt mutmut
    - name: Run mutation tests
      run: |
        mutmut run --paths-to-mutate=src/ || true
        mutmut results
    - name: Check mutation score
      run: |
        # Parse mutmut results and fail if below threshold
        SCORE=$(mutmut results | grep "Killed" | awk '{print $2}')
        if [ "$SCORE" -lt 850 ]; then  # 85% kill rate
          echo "Mutation score too low: ${SCORE}/1000"
          exit 1
        fi
```

### 46.4 Arid Node Configuration

Not all code benefits from mutation testing. Configure mutmut to skip "arid nodes" — AST nodes where mutants are unproductive:

**pyproject.toml:**
```toml
[tool.mutmut]
source_paths = ["src"]
backup = false
runner = "python -m pytest"

[tool.mutmut.exclude]
# Skip these — mutants here don't produce useful signals
do_not_mutate_patterns = [
    "__repr__",
    "__str__",
    "__init__",
    "log_*",
    "_log_*",
]

do_not_mutate = [
    "src/core/logging.py",
    "src/core/config.py",
]
```

> In-file exclusion: append `# pragma: no mutate` to any line mutmut should leave alone. (The old `paths_to_mutate` / `[tool.mutmut.exclude] functions/paths` keys are superseded by `source_paths` / `do_not_mutate_patterns` / `do_not_mutate`.)

### 46.5 Arid Node Types to Skip

| Node Type | Why Skip | Example |
|-----------|----------|---------|
| **Logging statements** | Changing log messages doesn't affect behavior | `logger.info("Processing %s", id)` |
| **Error messages** | Changing error text doesn't change logic | `raise ValueError("Invalid input")` |
| **Tuning parameters** | Changing a constant without domain knowledge is noise | `TIMEOUT = 30` |
| **Mocked dependencies** | Mutating mock setup tests the mock, not the code | `mock_db.save.return_value = True` |
| **Idiomatic patterns** | Language idioms where any change is always a bug | `if items is None: items = []` |
| **Debug-only code** | Code that only runs in development | `if DEBUG: show_debug_panel()` |

### 46.6 Mutation Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| **90%+** | Excellent — tests are catching behavior changes | Maintain |
| **80-90%** | Good — some gaps, investigate survivors | Add tests for survivors |
| **70-80%** | Fair — significant untested behavior | Prioritize gap closure |
| **<70%** | Poor — tests are mostly worthless | Major test overhaul needed |

### 46.7 Targeting Mutation Testing

Don't mutation test the entire codebase every time. Target:

1. **Changed code** — Only mutation test files modified in the current PR
2. **Critical paths** — Auth, payment, data mutation — always mutation test
3. **New code** — 100% mutation score required for new functions
4. **Legacy code** — Mutation test incrementally as you refactor

```bash
# Mutation test only changed files
git diff --name-only HEAD~1 | grep '\.py$' | grep -v tests/ | xargs mutmut run
```

---

