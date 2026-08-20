# Skill 29: Operational Patterns

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 29. Operational Patterns

Production-hardened patterns for reliability and resilience.

### 29.1 Circuit Breaker Pattern

Prevents cascading failures by stopping requests to a failing service.

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"           # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout: float = 60.0,
        quota_reset_timeout: float = 3600.0
    ):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout
        self.quota_reset_timeout = quota_reset_timeout

        self.failures = 0
        self.successes = 0
        self.last_failure_time: datetime | None = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError(f"Circuit open for {func.__name__}")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _should_attempt_reset(self) -> bool:
        if self.last_failure_time is None:
            return True
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout

    def _on_success(self):
        self.failures = 0
        if self.state == CircuitState.HALF_OPEN:
            self.successes += 1
            if self.successes >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.successes = 0
        self.last_failure_time = None

    def _on_failure(self):
        self.failures += 1
        self.successes = 0
        self.last_failure_time = datetime.now()

        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN

class CircuitBreakerOpenError(Exception):
    """Raised when circuit is open and request is rejected."""
    pass

class CircuitBreakerManager:
    """Manages multiple circuit breakers for different services."""
    _instance: 'CircuitBreakerManager | None' = None

    def __init__(self):
        self._breakers: dict[str, CircuitBreaker] = {}

    @classmethod
    def get_instance(cls) -> 'CircuitBreakerManager':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_breaker(self, name: str, **kwargs) -> CircuitBreaker:
        if name not in self._breakers:
            self._breakers[name] = CircuitBreaker(**kwargs)
        return self._breakers[name]
```

**When to use:**
- External API calls that may fail intermittently
- Database connections that can time out
- Any service call where failure is possible and cascading failures are dangerous

**Configuration guidelines:**
- `failure_threshold=5` — Open after 5 consecutive failures
- `success_threshold=2` — Close after 2 successes in half-open
- `timeout=60` — Try reset after 60 seconds

---

### 29.2 Dead Letter Queue (DLQ) Pattern

Handles background task failures with retry and escalation.

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import random

class DLQStatus(Enum):
    FAILED = "failed"
    RETRYING = "retrying"
    DEAD = "dead"
    RESOLVED = "resolved"

@dataclass
class DLQEntry:
    id: int
    task_name: str
    payload: dict
    status: DLQStatus
    attempts: int
    max_attempts: int
    next_retry: datetime
    created_at: datetime
    last_error: str | None

class DeadLetterQueue:
    def __init__(
        self,
        db_session,
        max_attempts: int = 5,
        base_delay: float = 1.0,
        max_delay: float = 60.0
    ):
        self.db = db_session
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay

    def enqueue(self, task_name: str, payload: dict, error: str):
        """Add failed task to DLQ."""
        entry = DLQEntry(
            id=None,
            task_name=task_name,
            payload=payload,
            status=DLQStatus.FAILED,
            attempts=1,
            max_attempts=self.max_attempts,
            next_retry=datetime.now() + timedelta(seconds=self.base_delay),
            created_at=datetime.now(),
            last_error=error
        )
        self.db.add(entry)
        self.db.commit()

    def process(self, handler: Callable[[dict], Any]) -> list[dict]:
        """Process DLQ entries with exponential backoff."""
        processed = []
        now = datetime.now()

        entries = self.db.query(DLQEntry).filter(
            DLQEntry.status.in_([DLQStatus.FAILED, DLQStatus.RETRYING]),
            DLQEntry.next_retry <= now,
            DLQEntry.attempts < DLQEntry.max_attempts
        ).all()

        for entry in entries:
            try:
                handler(entry.payload)
                entry.status = DLQStatus.RESOLVED
                processed.append({"id": entry.id, "status": "resolved"})
            except Exception as e:
                self._handle_failure(entry, str(e))

        self.db.commit()
        return processed

    def _handle_failure(self, entry: DLQEntry, error: str):
        entry.attempts += 1
        entry.last_error = error

        if entry.attempts >= entry.max_attempts:
            entry.status = DLQStatus.DEAD
        else:
            entry.status = DLQStatus.RETRYING
            delay = min(self.base_delay * (2 ** entry.attempts), self.max_delay)
            delay += random.uniform(0, 0.1 * delay)
            entry.next_retry = datetime.now() + timedelta(seconds=delay)

    def get_stats(self) -> dict:
        """Get DLQ statistics for monitoring."""
        return {
            "failed": self.db.query(DLQEntry).filter_by(status=DLQStatus.FAILED).count(),
            "retrying": self.db.query(DLQEntry).filter_by(status=DLQStatus.RETRYING).count(),
            "dead": self.db.query(DLQEntry).filter_by(status=DLQStatus.DEAD).count(),
            "resolved": self.db.query(DLQEntry).filter_by(status=DLQStatus.RESOLVED).count(),
        }
```

**When to use:**
- Background tasks that can fail intermittently
- Tasks where failure should not block the main request
- Any async job that needs retry with backoff

---

### 29.3 Middleware Stack Pattern

Layer multiple concerns cleanly with a middleware chain.

```python
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import time
import asyncio
import logging

logger = logging.getLogger(__name__)

# 1. Request ID Middleware — UUID propagation
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

# 2. Request Size Middleware — Prevent large payloads
class RequestSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_size: int = 10 * 1024 * 1024):
        super().__init__(app)
        self.max_size = max_size

    async def dispatch(self, request: Request, call_next):
        if request.method in ("POST", "PUT", "PATCH"):
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.max_size:
                return Response(content="Request too large", status_code=413)
        return await call_next(request)

# 3. Request Timeout Middleware
class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout: float = 30.0):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next):
        try:
            response = await asyncio.wait_for(call_next(request), timeout=self.timeout)
            return response
        except asyncio.TimeoutError:
            return Response(content="Request timeout", status_code=504)

# 4. Slow Query Middleware — Log slow requests
class SlowQueryMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, threshold: float = 1.0):
        super().__init__(app)
        self.threshold = threshold

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        if duration > self.threshold:
            logger.warning(
                f"Slow request: {request.method} {request.url.path} "
                f"took {duration:.2f}s [request_id={getattr(request.state, 'request_id', '')}]"
            )
        return response

# 5. Metrics Middleware — Prometheus-style metrics
class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests_total = {}
        self.request_durations = []

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        key = f"{request.method}_{request.url.path}"
        self.requests_total[key] = self.requests_total.get(key, 0) + 1
        self.request_durations.append(duration)

        return response

# Register all middleware in order
app = FastAPI()
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RequestSizeMiddleware)
app.add_middleware(TimeoutMiddleware)
app.add_middleware(SlowQueryMiddleware)
app.add_middleware(MetricsMiddleware)
```

**Middleware order matters:**
1. RequestID (first, sets up tracing)
2. RequestSize (validate before processing)
3. Timeout (prevent hanging requests)
4. SlowQuery (measure after processing)
5. Metrics (record after everything)

---

### 29.4 Semantic Cache Pattern

LRU cache with TTL and optional Redis backend.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any
import hashlib
import json

@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: datetime
    ttl: int
    hits: int = 0

    def is_expired(self) -> bool:
        return (datetime.now() - self.created_at).total_seconds() > self.ttl

class SemanticCache:
    """LRU cache with TTL, optional Redis backend."""

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: dict[str, CacheEntry] = {}

    def _make_key(self, data: dict) -> str:
        normalized = json.dumps(data, sort_keys=True)
        return hashlib.md5(normalized.encode()).hexdigest()

    def get(self, data: dict) -> Any | None:
        key = self._make_key(data)
        entry = self.cache.get(key)
        if entry is None or entry.is_expired():
            if entry:
                del self.cache[key]
            return None
        entry.hits += 1
        return entry.value

    def set(self, data: dict, value: Any, ttl: int | None = None):
        key = self._make_key(data)
        if len(self.cache) >= self.max_size:
            lru_key = min(self.cache, key=lambda k: self.cache[k].hits)
            del self.cache[lru_key]
        self.cache[key] = CacheEntry(
            key=key, value=value,
            created_at=datetime.now(),
            ttl=ttl or self.default_ttl
        )

    def invalidate(self, pattern: str | None = None):
        if pattern is None:
            self.cache.clear()
        else:
            keys_to_remove = [k for k in self.cache if pattern in k]
            for key in keys_to_remove:
                del self.cache[key]

    def get_stats(self) -> dict:
        total_hits = sum(e.hits for e in self.cache.values())
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "total_hits": total_hits,
        }
```

---

