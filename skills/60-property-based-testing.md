# Skill 60: Property-Based Testing

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 60. Property-Based Testing

Example-based tests prove a function works for the cases you thought of. Property-based tests prove it for hundreds of generated cases and find edge cases you didn't think of — by shrinking failures to the minimal repro.

### 60.1 When to Use

- **Pure logic**: parsers, serializers, validators, math, sorting, deduplication, boundary logic.
- **Invariants that hold for ALL inputs**: `round-trip(x) == x`, `sorted(list).length == list.length`, `validate(validated) == validated`.
- **API/contract properties**: a parse→serialize round-trip, error on invalid input, idempotency.
- Not a substitute for behavioral example tests; it complements them ([Section 8](skills/08-testing-requirements.md)).

### 60.2 Basic Patterns (Hypothesis)

```python
from hypothesis import given, strategies as st, settings, HealthCheck

@given(st.lists(st.integers()))
def test_sort_is_stable_length(xs: list[int]) -> None:
    out = sorted(xs)
    assert len(out) == len(xs)

@given(st.text())
def test_round_trip(s: str) -> None:
    assert deserialize(serialize(s)) == s
```

- Start with built-in strategies (`st.integers`, `st.text`, `st.lists`, `st.dictionaries`, `st.one_of`, `st.builds(MyModel)`).
- Add custom strategies (`@st.composite`) for domain-shaped data (valid emails, constrained IDs).
- Keep the strategy close to the real input domain; a strategy that always generates valid input hides the edge you care about.

### 60.3 Shrinking & Seeds

- **Shrinking** reduces a failing case to the smallest repro — trust it, and record the shrunk case as a regression test.
- **Seeds**: pin the failing seed for CI by passing `--hypothesis-seed=<n>` or recording it in the failure output. This makes a flaky/rare failure reproducible.
- Hypothesis emits "Falsifying example" + seed on failure — capture both.

### 60.4 Running in CI

- Property tests are slower than unit tests — keep them in a separate marker/tag (`@pytest.mark.property`) or separate file so the fast suite stays fast.
- Give Hypothesis a time/size budget per run rather than an unbounded count:
  ```toml
  [tool.pytest.ini_options]
  markers = ["property: property-based tests"]
  ```
  ```python
  @settings(max_examples=200, deadline=2000, suppress_health_check=[HealthCheck.too_slow])
  def test_...: ...
  ```
- In CI, run the property suite too — they are the tests most likely to catch cross-platform/ordering/unicode edge cases.

### 60.5 Pitfalls

- **Over-generation**: generating huge inputs slows the suite; bound size (`max_size`, `max_leaves`).
- **Weak properties**: an assertion that can't fail is noise ([Section 24.10](skills/24-common-failure-modes.md)). Each property must be falsifiable.
- **Health-check noise**: `suppress_health_check` is a tool, not a habit — only suppress when the strategy legitimately needs it.
- **Non-deterministic functions** (time, random, network) must be faked/seeded before property testing, or tests fail for the wrong reason.

---

## References

- Hypothesis — https://hypothesis.readthedocs.io/en/latest/
