# Skill 62: Retries, Backoff & Idempotency

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 62. Retries, Backoff & Idempotency

Retrying a failed network call without design is how outages become cascades (thundering herd) and how money gets charged twice. Retries are only safe when the operation is idempotent or keyed, and only sane with backoff + jitter + budgets.

### 62.1 What to Retry

- Retry **transient** failures only: timeouts, connection resets, `429` (with `Retry-After`), `5xx`.
- **NEVER** retry a client error (`4xx`) — retrying a `400`/`401`/`403` is wasted load and can look like an attack.
- **NEVER** blindly retry non-idempotent operations (POST that creates a record) without an idempotency key (Section 62.4).
- On `429`/`503`, honor `Retry-After`; back off harder than the server asks.

### 62.2 Exponential Backoff with Jitter

- Backoff grows exponentially: `delay = base * (2 ** attempt)` with a cap.
- **Add jitter** (full jitter: `random() * delay`) so synchronized failures don't stampede the downstream service.
- Set a total budget: max attempts (e.g. 3-5) and max wall-clock time. Give up, fail fast, and surface the error — a forever-retrying worker is a zombie ([Section 24.7](skills/24-common-failure-modes.md)).
- Use proven libraries rather than hand-rolling: `tenacity`, `backoff`, `pybreaker`/`cockatiel` ([Section 29](skills/29-operational-patterns.md)).

```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type
import httpx

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential_jitter(initial=0.5, max=10),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
)
def call_api() -> httpx.Response: ...
```

### 62.3 Retry-After & Rate Limits

- Parse `Retry-After` (seconds or HTTP-date) and back off by at least that long.
- Track rate-limit headers (`X-RateLimit-Remaining`/`X-RateLimit-Reset` where present).
- Circuit breaker: after repeated failures, stop trying for a cooldown window instead of hammering ([Section 29](skills/29-operational-patterns.md)).

### 62.4 Idempotency Keys

For side-effecting operations (payments, webhook deliveries, order creation):

- Client sends `Idempotency-Key: <uuid>`; the server dedupes — if the same key repeats, return the original result instead of re-executing.
- The Stripe pattern: the key is bound to a specific operation's result, so a retried request can't double-charge.
- Store key→result with a TTL; return `409` or the cached result on collision depending on API contract.
- **Rule**: if you retry a write, the retried request MUST carry the same idempotency key, or it isn't a retry — it's a second operation.

### 62.5 Timeouts

- **Every outbound call needs a timeout** (connect + read + total). No timeout = a hung worker holding resources forever ([Section 20](skills/20-external-integrations.md)).
- Keep timeouts shorter than the caller's timeout so the chain doesn't pile up.
- Propagate deadlines/context across the call chain so cancellation actually cancels ([Section 29.5](skills/29-operational-patterns.md)).

### 62.6 Rules (NEVER additions)

- **NEVER** retry without checking idempotency for side-effecting calls.
- **NEVER** use zero backoff or fixed rapid retries — that's a self-inflicted DDoS.
- **NEVER** retry past the total budget and then silently swallow — log and escalate ([Section 59](skills/59-incident-response-and-runbooks.md)).
- **NEVER** hand-roll retry loops when a battle-tested library exists ([Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md) decision ladder).

---

## References

- Stripe idempotency keys — https://docs.stripe.com/api/idempotent_requests
