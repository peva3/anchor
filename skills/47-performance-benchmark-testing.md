# Skill 47: Performance Benchmark Testing

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 47. Performance Benchmark Testing

Performance regressions are bugs. They should be caught in CI, not in production by users complaining about slowness.

### 47.1 Setup with pytest-benchmark

```bash
pip install pytest-benchmark
```

```python
# tests/benchmarks/test_performance.py
import pytest

def test_model_scoring_benchmark(benchmark):
    """Scoring 1000 items must complete under 50ms."""
    items = generate_test_items(1000)

    result = benchmark(scoring_function, items)

    assert result is not None

def test_db_query_benchmark(benchmark, db_session):
    """List query with 10k rows must complete under 100ms."""
    # Populate test data
    for i in range(10_000):
        db_session.add(Item(name=f"item_{i}"))
    db_session.commit()

    result = benchmark(
        lambda: db_session.query(Item).filter(Item.name.like("item_99%")).all()
    )

    assert len(result) > 0

def test_api_endpoint_benchmark(benchmark, client):
    """GET /api/items must complete under 30ms p95."""
    response = benchmark(client.get, "/api/items?limit=50")
    assert response.status_code == 200
```

### 47.2 Time Budget Assertions

```python
def test_critical_path_with_time_budget(benchmark):
    """Critical path operations have hard time budgets."""
    budget_ms = {
        "validate_token": 5,
        "check_permission": 10,
        "fetch_user": 20,
        "serialize_response": 5,
    }

    for operation, max_ms in budget_ms.items():
        fn = get_operation(operation)
        benchmark.name = f"time_budget_{operation}"

        result = benchmark(fn, test_input())

        # Assert median time is within budget
        stats = benchmark.stats
        assert stats.stats.median < max_ms / 1000.0, \
            f"{operation}: median {stats.stats.median*1000:.1f}ms exceeds budget {max_ms}ms"
```

### 47.3 CI Integration

```yaml
# Performance regression detection in CI
benchmark:
  name: Performance Benchmarks
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2

    - name: Run benchmarks
      run: |
        pytest tests/benchmarks/ \
          --benchmark-only \
          --benchmark-json=benchmark_results.json \
          --benchmark-autosave

    - name: Compare against baseline
      run: |
        pytest-benchmark compare HEAD~1 HEAD --group-by=name

    - name: Fail on regression
      run: |
        # Parse results and fail if any benchmark regressed >10%
        python scripts/check_benchmark_regression.py benchmark_results.json

    - name: Store benchmark results
      uses: benchmark-action/github-action-benchmark@v1
      with:
        tool: pytest
        output-file-path: benchmark_results.json
        alert-threshold: 120%  # Alert if >20% regression
        comment-on-alert: true
        fail-on-alert: true
        auto-push: false
```

### 47.4 What to Benchmark

| Category | What to Measure | Target |
|----------|----------------|--------|
| **API endpoints** | Response time p50, p95, p99 | <50ms p95 for reads, <200ms p95 for writes |
| **Database queries** | Query execution time | <20ms for simple queries, <100ms for joins |
| **Serialization** | JSON parse + serialize | <5ms for typical payload |
| **Authentication** | Token validation | <10ms |
| **Cache operations** | Get/Set operations | <2ms |
| **Startup time** | Application boot to first request | <5s |
| **Memory usage** | RSS after warmup | <500MB baseline |

### 47.5 NEVER Do These for Benchmarks

- **NEVER** run benchmarks on oversubscribed CI runners — use dedicated runners or control for noise
- **NEVER** compare benchmarks across different machines — always use same hardware
- **NEVER** accept a 20%+ regression without investigation
- **NEVER** benchmark with unrealistic data volumes — test with production-scale data
- **NEVER** benchmark only happy paths — measure worst-case performance too
- **NEVER** skip benchmarking "because the change is small" — small changes cause big regressions

---

