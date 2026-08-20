# Skill 49: Chaos Engineering

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 49. Chaos Engineering

Chaos engineering validates that systems behave correctly under failure conditions. It is NOT random destruction — it is controlled experimentation.

### 49.1 Principles (from Netflix Chaos Engineering)

1. **Define "steady state"** — Metrics that represent normal behavior
2. **Hypothesize** — Steady state will continue in both control and experimental groups
3. **Introduce variables** — Simulate real-world failures (server crashes, network latency, resource exhaustion)
4. **Disprove hypothesis** — Look for deviations from steady state
5. **Minimize blast radius** — Start small, expand gradually

### 49.2 Experiment Design Template

Every chaos experiment MUST follow this template:

```yaml
experiment:
  name: Database Connection Failure
  hypothesis: >
    When the primary database becomes unreachable for 30 seconds,
    the application will serve stale data from cache and reconnect
    automatically within 5 seconds of database recovery.
  steady_state_metrics:
    - p95_latency_ms < 200
    - error_rate < 0.01
    - cache_hit_ratio > 0.50
  method:
    - type: network_partition
      target: database
      duration_seconds: 30
  blast_radius:
    - environment: staging
    - affected_services: [api]
    - unaffected_services: [background_worker]
  rollback:
    trigger: error_rate > 0.10 OR p95_latency_ms > 1000 OR duration > 120
    action: restore_network
  success_criteria:
    - error_rate stayed below 0.05
    - p95_latency_ms stayed below 500
    - No data corruption detected
    - Application reconnected within 5s of database recovery
```

### 49.3 Failure Injection Patterns

```python
import asyncio
import random
from contextlib import asynccontextmanager
from typing import Callable, Awaitable

class FailureInjector:
    """Inject controlled failures for chaos testing."""

    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    @asynccontextmanager
    async def latency(self, min_ms: int = 50, max_ms: int = 500):
        """Inject random latency into an operation."""
        if self.enabled:
            delay = random.uniform(min_ms, max_ms) / 1000
            await asyncio.sleep(delay)
        yield

    async def maybe_fail(self, failure_rate: float = 0.1, error_type: type = Exception):
        """Fail with given probability."""
        if self.enabled and random.random() < failure_rate:
            raise error_type("Chaos monkey says no")

    async def maybe_timeout(self, timeout_rate: float = 0.1, duration_s: float = 30):
        """Timeout with given probability."""
        if self.enabled and random.random() < timeout_rate:
            await asyncio.sleep(duration_s)
            raise TimeoutError("Chaos timeout")

# Usage in production code (gated by config)
chaos = FailureInjector(enabled=config.CHAOS_ENGINEERING_ENABLED)

async def fetch_data_from_db(query: str):
    await chaos.maybe_fail(failure_rate=0.05, error_type=ConnectionError)
    async with chaos.latency(min_ms=10, max_ms=200):
        return await db.execute(query)
```

### 49.4 Chaos Experiment Library

| Experiment | What It Tests | How to Run |
|-----------|---------------|------------|
| **Kill a service** | Failover, health checks, graceful degradation | `docker compose stop <service>` |
| **Network latency** | Timeout handling, retry logic | `tc qdisc add dev eth0 root netem delay 500ms` |
| **Network partition** | Service isolation, split-brain prevention | `iptables -A INPUT -s <service_ip> -j DROP` |
| **CPU exhaustion** | Throttling, resource limits, priority scheduling | `stress --cpu 4 --timeout 60s` |
| **Memory exhaustion** | OOM handling, graceful degradation | `stress --vm 2 --vm-bytes 1G --timeout 60s` |
| **Disk full** | Error handling, cleanup, alerting | `dd if=/dev/zero of=/tmp/fill bs=1M count=1000` |
| **DNS failure** | Caching, fallback IPs | `iptables -A OUTPUT -p udp --dport 53 -j DROP` |
| **Dependency slow** | Circuit breaker, timeout configuration | Inject latency at proxy level |
| **Clock skew** | Time-based logic, token expiry | Change system clock by ±5 minutes |
| **Certificate expiry** | TLS handling, renewal automation | Use short-lived certs in staging |

### 49.5 Game Day Checklist

**Before game day:**
- [ ] All observability tooling is in place (logs, metrics, traces, alerts)
- [ ] Steady state metrics are defined and measurable
- [ ] Blast radius is minimized (start with staging, one service)
- [ ] Rollback plan is documented and tested
- [ ] Communication channel is established (Slack channel, incident bridge)
- [ ] All team members know the experiment is running

**During game day:**
- [ ] Announce experiment start
- [ ] Inject failure
- [ ] Observe system response (monitor dashboards)
- [ ] Document observations in real time
- [ ] If steady state is violated beyond hypothesis, abort immediately
- [ ] Announce experiment end

**After game day:**
- [ ] Write post-mortem: what happened, what was learned, what needs to change
- [ ] Create action items for any weaknesses discovered
- [ ] Schedule fix implementation
- [ ] Re-run experiment after fixes to verify improvement
- [ ] Share learnings with the team

### 49.6 Chaos Engineering Readiness

Don't start chaos engineering unless:
- [ ] You have comprehensive monitoring (metrics, logs, traces)
- [ ] You have defined SLOs and steady state metrics
- [ ] You have automated rollback/deployment
- [ ] Your on-call rotation is established
- [ ] You have run failure mode analysis (FMEA) on your architecture
- [ ] Your blast radius can be contained to non-production environments first

**Start simple:**
1. First experiment: Kill a non-critical service in staging. Observe.
2. Second: Add network latency to staging database. Observe.
3. Third: Fill staging disk to 90%. Observe.
4. Fourth: Move to production with minimal blast radius.
5. Continue expanding scope as confidence grows.

---

