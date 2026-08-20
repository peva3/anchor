# Skill 49: Chaos Engineering

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

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

### 49.3 Failure Injection Tools

Prefer battle-tested tools over hand-rolled `tc`/`iptables` snippets — those require root and don't work in containers, on macOS, or on managed CI. The in-app `FailureInjector` class is a reinvention; standard tooling covers the same ground.

| Tool | Use For |
|------|---------|
| **Chaos Mesh** | Kubernetes-native fault injection (network, disk, pod kill, time) via CRDs |
| **LitmusChaos** | Kubernetes chaos experiments with git-ops experiment definitions |
| **AWS Fault Injection Simulator (FIS)** | AWS resources (EC2, EKS, RDS, network) with safe defaults and guardrails |
| **Toxiproxy** | TCP-level fault proxy for app-level latency/down/blackhole — works in containers and local dev |
| **stress / stress-ng** | CPU, memory, disk I/O resource exhaustion |

```bash
# Toxiproxy: inject 500ms latency into a connection (works in CI/local)
toxiproxy-cli create db -l localhost:12345 -u db:5432
toxiproxy-cli toxic add db -t latency -a latency=500

# Chaos Mesh: inject network partition into the api pod (staging)
#   kubectl apply -f network-partition.yaml  # with targetSelector: api
```

> If you keep an in-app failure injector (e.g. for unit-level chaos), gate it behind config and NEVER ship it enabled to production — a `FailureInjector(enabled=True)` in prod is itself a production incident.

### 49.4 Chaos Experiment Library

| Experiment | What It Tests | How to Run |
|-----------|---------------|------------|
| **Kill a service** | Failover, health checks, graceful degradation | `docker compose stop <service>` or Chaos Mesh PodKill |
| **Network latency** | Timeout handling, retry logic | Toxiproxy latency toxic, or Chaos Mesh NetworkChaos (not raw `tc`) |
| **Network partition** | Service isolation, split-brain prevention | Chaos Mesh / Litmus network partition, or AWS FIS |
| **CPU exhaustion** | Throttling, resource limits, priority scheduling | `stress --cpu 4 --timeout 60s` |
| **Memory exhaustion** | OOM handling, graceful degradation | `stress --vm 2 --vm-bytes 1G --timeout 60s` |
| **Disk full** | Error handling, cleanup, alerting | Fill the volume in staging only |
| **DNS failure** | Caching, fallback IPs | Chaos Mesh / Toxiproxy proxy, or fail the resolver in staging |
| **Dependency slow** | Circuit breaker, timeout configuration | Inject latency at proxy level (Toxiproxy) |
| **Clock skew** | Time-based logic, token expiry | Change system clock by ±5 minutes (staging VMs only) |
| **Certificate expiry** | TLS handling, renewal automation | Use short-lived certs in staging |

### 49.5 Game Day Checklist

**Before game day:**
- [ ] All observability tooling is in place (logs, metrics, traces, alerts)
- [ ] Steady state metrics are defined and measurable
- [ ] Blast radius is minimized (start with staging, one service)
- [ ] Rollback plan is documented and tested
- [ ] Communication channel is established (Slack channel, incident bridge)
- [ ] All team members know the experiment is running
- [ ] **PRODUCTION experiments require explicit human approval** ([Section 36.4](skills/36-explicit-prohibitions-the-never-list.md) — never spend money or risk production without explicit user authorization), a documented window, and a named on-call owner

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

