# Skill 45: Flaky Test Management

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 45. Flaky Test Management

Flaky tests (tests that pass and fail intermittently without code changes) erode trust in the test suite. They are a top cause of CI burnout and deployment delays.

### 45.1 Four Sources of Flakiness (Google Classification)

| Source | Example | Frequency |
|--------|---------|-----------|
| **The tests themselves** | Improper initialization, ordering dependencies, race conditions in test code | Most common |
| **The test framework** | Resource allocation errors, scheduling collisions, test runner bugs | Uncommon |
| **The application (SUT)** | Slow responses, memory leaks, genuine non-determinism | Common |
| **OS/hardware/network** | Network instability, disk errors, CI resource exhaustion | Common in CI |

### 45.2 Flaky Test Detection

```ini
# pytest.ini
[pytest]
# Re-run failed tests to detect flakiness (CI only — see 45.2b)
addopts =
    --reruns 2
    --reruns-delay 1
    --only-rerun "AssertionError"
    --only-rerun "TimeoutError"
```

```bash
# Install rerun plugin
pip install pytest-rerunfailures

# Run tests with retry (detects flaky tests)
pytest --reruns 3 --reruns-delay 1

# Create a report of flaky tests
pytest --reruns 3 --rerun-flaky-report=flaky_report.json
```

**45.2b Reruns are CI-only, and only for diagnosis:**
- Re-running masks flakes locally — set reruns in the CI config (or via `PYTEST_ADDOPTS`), NOT in committed `pytest.ini`, so a developer's local failure is a real failure
- A test that only passes on the retry is still flaky — log it as a flaky report and root-cause it (Section 45.3), don't just accept the rerun
- `pytest-rerunfailures` is **incompatible** with `pytest-xdist --looponfail`, `--pdb`, and the `flaky` plugin — don't combine them

**45.2c Detect order-dependence with `pytest-randomly`:**
Install `pytest-randomly` and run CI with random ordering (`pytest-randomly` shuffles test order and the seed is printed). If a test fails under shuffle, it's order-dependent — fix the isolation, don't pin the seed to hide it. Keep the seed in the failure output so you can reproduce.

### 45.3 Quarantine Mechanism

When a flaky test is discovered, quarantine it immediately — do NOT delete it:

```python
import pytest

@pytest.mark.flaky(reason="Intermittent timeout in CI, ticket #1234")
def test_thing_that_flakes():
    """This test is quarantined — it does NOT block CI but IS tracked."""
    result = do_something()
    assert result is not None
```

```ini
# pytest.ini — register the marker AND exclude quarantined tests from CI
[pytest]
markers =
    flaky: Test is known to be flaky (see ticket for details)
addopts =
    -m "not flaky"        # quarantined tests are excluded by default
```

> Without `-m "not flaky"` in CI, the marker only labels tests — they still run and still block CI. Exclude them, then make sure a scheduled/lab job runs `-m flaky` so they keep being exercised while quarantined.

**Quarantine process:**
1. **Detect** — Identify flaky test from CI failures
2. **Quarantine** — Add `@pytest.mark.flaky` marker with reason and ticket reference
3. **Track** — Create an issue to fix the flaky test within 7 days
4. **Fix** — Root-cause the flakiness (not just re-run)
5. **Unquarantine** — Remove the marker after the fix is verified stable for 10+ CI runs

### 45.4 Remediation Strategies

| Problem | Wrong Fix | Right Fix |
|---------|-----------|-----------|
| **Ordering dependency** | Renumber tests to run in order | Make each test create its own fixtures, use `@pytest.fixture(autouse=False)` |
| **Shared mutable state** | Add `time.sleep(1)` between tests | Reset state in fixture teardown, isolate test data by test |
| **Time-dependent tests** | Use wide time tolerances (e.g., ±5s) | Freeze time with `freezegun` or inject a clock |
| **External dependency flaky** | Skip test if external service is down | Mock external services, add contract tests for actual integration |
| **Race condition in app** | Increase test timeout | Fix the race condition (add proper synchronization) |
| **CI resource contention** | Run tests sequentially | Profile test resource usage, add resource requests/limits |

### 45.5 NEVER Do These for Flaky Tests

- **NEVER** delete a failing or flaky test without understanding why it failed — quarantine it first (Section 45.3), then root-cause within 7 days
- **NEVER** add `time.sleep()` to a test — fix the synchronization, don't paper over it
- **NEVER** increase a timeout arbitrarily — understand why it's slow
- **NEVER** mark a test as "known flaky" without creating a fix ticket — quarantine expires
- **NEVER** skip a flaky test without a documented reason
- **NEVER** allow flaky tests to accumulate — fix them within SLA (7 days)

### 45.6 Test Isolation Principles

Every test must be:
- **Independent** — Can run in any order, in parallel, or alone
- **Self-contained** — Creates its own fixtures, doesn't depend on prior test state
- **Deterministic** — Same inputs produce same outputs every run
- **Hermetic** — No external dependencies (network, database, filesystem) unless explicitly an integration test
- **Fast** — Unit tests < 1s each, integration tests < 10s each

```python
# CORRECT — isolated test
@pytest.fixture
def fresh_user():
    """Each test gets its own user — no shared state."""
    return User(name="Test User", email="test@example.com")

def test_user_creation(fresh_user):
    assert fresh_user.name == "Test User"

def test_user_email_update(fresh_user):
    fresh_user.email = "updated@example.com"
    assert fresh_user.email == "updated@example.com"
    # Does NOT affect test_user_creation — they get different fixtures

# WRONG — interdependent tests
created_user_id = None

def test_create_user():
    global created_user_id
    user = create_user("Alice")
    created_user_id = user.id
    assert user.id is not None

def test_update_user():
    # DEPENDS on test_create_user running first — will fail if run alone
    update_user(created_user_id, name="Bob")
```

---

