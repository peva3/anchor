# Skill 41: Observability Standards

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 41. Observability Standards

Production systems require structured observability — you cannot debug what you cannot see.

### 41.1 Structured Logging

ALL logs in production MUST be structured JSON, not human-readable text.

```python
import json
import logging
from datetime import datetime, timezone
from typing import Any
import uuid

class JSONFormatter(logging.Formatter):
    """Format logs as structured JSON for machine processing."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Include trace context if available
        if hasattr(record, "trace_id"):
            log_entry["trace_id"] = record.trace_id
        if hasattr(record, "span_id"):
            log_entry["span_id"] = record.span_id
        if hasattr(record, "correlation_id"):
            log_entry["correlation_id"] = record.correlation_id

        # Include exception info if present
        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = {
                "type": type(record.exc_info[1]).__name__,
                "message": str(record.exc_info[1]),
            }

        # Include extra fields passed via log call
        if hasattr(record, "extra_fields"):
            log_entry.update(record.extra_fields)

        return json.dumps(log_entry)

# Setup
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(handler)
```

**Log level usage:**
| Level | When to Use | Example |
|-------|-------------|---------|
| **DEBUG** | Per-request details, internal state transitions | "Cache hit for key abc123" |
| **INFO** | Business operations, lifecycle events | "Processed batch of 42 items in 1.2s" |
| **WARNING** | Recoverable issues, degraded state | "Retry 2/3 after timeout (123ms)" |
| **ERROR** | Failures that need investigation | "Failed to connect to database after 3 retries" |
| **CRITICAL** | System-level failures | "Out of disk space, cannot continue" |

### 41.2 Distributed Tracing with OpenTelemetry

Every service MUST propagate trace context across boundaries.

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

def setup_tracing(service_name: str, otlp_endpoint: str):
    """Initialize OpenTelemetry tracing for this service."""
    # Configure via standard SDK env vars instead of code when possible:
    #   OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_SERVICE_NAME,
    #   OTEL_RESOURCE_ATTRIBUTES, OTEL_PROPAGATORS, OTEL_TRACES_SAMPLER
    from opentelemetry.sdk.resources import Resource
    tracer_provider = TracerProvider(
        resource=Resource.create({"service.name": service_name})
    )

    # Prefer TLS (no insecure=True — deprecated in the OTLP exporter).
    # For plaintext dev endpoints pass insecure=True explicitly and add a TODO
    # to switch to OTEL_EXPORTER_OTLP_ENDPOINT=https://... in prod.
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(exporter))

    # Set global tracer provider
    trace.set_tracer_provider(tracer_provider)

    # Auto-instrument libraries
    FastAPIInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    RedisInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument()

    return trace.get_tracer(service_name)

# Usage — create spans for custom operations
tracer = setup_tracing("my-service", "http://otel-collector:4317")

async def process_order(order_id: str):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        span.add_event("order.validated", {"items": 3})

        # Nested spans for sub-operations
        with tracer.start_as_current_span("charge_payment"):
            result = await charge(order_id)

        span.set_attribute("order.status", result.status)
        return result
```

### 41.3 Prometheus Metrics

Standard metrics every service MUST export:

```python
from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_client import generate_latest, REGISTRY

# REQUIRED metrics for any web service
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

REQUEST_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Currently in-flight HTTP requests"
)

ERROR_COUNT = Counter(
    "errors_total",
    "Total errors by type",
    ["error_type", "service"]
)

# Application-specific metrics
DB_QUERY_DURATION = Histogram(
    "db_query_duration_seconds",
    "Database query duration",
    ["operation", "table"]
)

CACHE_HIT_RATIO = Gauge(
    "cache_hit_ratio",
    "Cache hit ratio (0.0-1.0)"
)

TASK_QUEUE_SIZE = Gauge(
    "task_queue_size",
    "Number of tasks waiting in queue",
    ["queue_name"]
)

# Expose metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(REGISTRY),
        media_type="text/plain"
    )
```

### 41.4 Correlation IDs

Every request MUST carry a correlation ID through the entire system. When OpenTelemetry is in use, prefer propagating the W3C `traceparent` header (via `OTEL_PROPAGATORS=tracecontext,baggage`) so traces link across services; the custom `X-Correlation-ID` middleware below is the fallback for systems without a tracer.

```python
from contextvars import ContextVar

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Extract or generate correlation ID for every request."""

    async def dispatch(self, request: Request, call_next):
        # Extract from header or generate new
        correlation_id = request.headers.get(
            "X-Correlation-ID",
            request.headers.get("X-Request-ID", str(uuid.uuid4()))
        )

        # Set in context var for this request
        correlation_id_var.set(correlation_id)

        # Propagate to downstream calls via context
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response
```

### 41.5 PII Redaction in Logs

NEVER log personally identifiable information. Implement automatic redaction:

```python
import re

PII_PATTERNS = [
    (r'\b[\w\.-]+@[\w\.-]+\.\w{2,}\b', '[EMAIL]'),              # Email
    (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]'),                        # SSN
    (r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CC]'),   # Credit card
    (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP]'),       # IP (in user content)
    (r'Bearer\s+[A-Za-z0-9\-\._~\+\/]+=*', 'Bearer [TOKEN]'),   # Auth tokens
    (r'api[_-]?key[=:]\s*[A-Za-z0-9]+', 'api_key=[REDACTED]'),  # API keys in params
]

def sanitize_for_logging(value: str) -> str:
    """Redact PII before logging."""
    for pattern, replacement in PII_PATTERNS:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return value

# Usage
logger.info("User input: %s", sanitize_for_logging(user_input))
```

### 41.6 Service Level Objectives (SLOs)

Define and monitor these for every production service:

| SLO | Target | Measurement |
|-----|--------|-------------|
| **Availability** | 99.9% | Successful requests / total requests |
| **Latency (p50)** | < 50ms | Median response time |
| **Latency (p95)** | < 200ms | 95th percentile response time |
| **Latency (p99)** | < 500ms | 99th percentile response time |
| **Error rate** | < 0.1% | Error responses / total responses |
| **Error budget burn rate** | < 1x | Rate of consuming error budget |

**Error budget:** If SLO is 99.9% availability, the error budget is 0.1%. This is ~43 minutes of allowed downtime per month. Track consumption.

---

