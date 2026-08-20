# Skill 30: Health Endpoint Specification

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 30. Health Endpoint Specification

Every production service MUST implement a comprehensive health check.

### 30.1 Health Check Design

```python
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import time

app = FastAPI()
start_time = time.time()

class SubsystemStatus(BaseModel):
    status: str
    message: str | None = None
    latency_ms: float | None = None

class HealthResponse(BaseModel):
    status: str
    version: str
    uptime_seconds: float
    subsystems: dict[str, SubsystemStatus]
    timestamp: str

@app.get("/health")
async def health_check() -> HealthResponse:
    subsystems = {}
    subsystems["database"] = await check_database()
    subsystems["cache"] = await check_cache()
    subsystems["external_api"] = await check_external_api()
    subsystems["background_tasks"] = check_background_tasks()
    subsystems["dlq"] = check_dlq_status()

    overall_status = determine_overall_status(subsystems)

    return HealthResponse(
        status=overall_status,
        version=get_version(),
        uptime_seconds=time.time() - start_time,
        subsystems=subsystems,
        timestamp=datetime.now().isoformat()
    )
```

### 30.2 What to Check Per Subsystem

| Subsystem | Check | Degraded | Unhealthy |
|-----------|-------|----------|-----------|
| **Database** | Query `SELECT 1` | >100ms | >1s or error |
| **Cache (Redis)** | `PING` command | >50ms | >500ms or error |
| **External API** | HTTP GET | >500ms | >2s or 5xx |
| **Background Tasks** | Count running vs max | >80% capacity | >100% |
| **DLQ** | Count dead letters | >100 dead | >1000 dead |
| **Disk** | Available space | <20% free | <10% free |
| **Memory** | RSS vs limit | >80% used | >95% used |

### 30.3 Response Format

```json
{
  "status": "degraded",
  "version": "1.2.3",
  "uptime_seconds": 86400,
  "timestamp": "2026-06-03T12:00:00Z",
  "subsystems": {
    "database": {"status": "healthy", "latency_ms": 12},
    "cache": {"status": "degraded", "message": "Redis PING took 450ms"},
    "external_api": {"status": "unhealthy", "message": "Connection timeout"}
  }
}
```

### 30.4 Kubernetes Probe Configuration

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30
  timeoutSeconds: 5
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
```

---

