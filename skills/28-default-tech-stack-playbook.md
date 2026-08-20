# Skill 28: Default Tech Stack Playbook

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 28. Default Tech Stack Playbook

Best-in-class recommendations for common project types, based on analysis of top GitHub projects (FastAPI, Next.js, Gin, etc.) and current industry trends.

### 28.1 How to Use This Playbook

When starting a new project, identify the project type below and use the recommended stack.
This playbook prioritizes:
- Production-proven technologies (Microsoft, Netflix, Uber use FastAPI)
- Strong ecosystem and community support
- Best performance per complexity ratio
- Async-first for I/O-bound workloads

---

### 28.2 REST APIs

#### Python API — FastAPI (RECOMMENDED)

**Stack:** FastAPI + Pydantic + Uvicorn + SQLAlchemy + PostgreSQL

**Evidence:** Microsoft, Uber, Netflix, Cisco use FastAPI in production. 98.9k GitHub stars.

```
project/
├── src/
│   ├── api/              # FastAPI routes
│   ├── models/           # Pydantic models (request/response)
│   ├── services/         # Business logic
│   └── core/             # Config, logging, database
├── tests/
├── alembic/              # DB migrations (if using SQLAlchemy)
└── docker-compose.yml
```

**Why FastAPI:**
- Auto-generated OpenAPI docs (Swagger UI)
- Type hints throughout (mypy-friendly)
- Async support (high throughput)
- Pydantic validation built-in
- Performance on par with Node.js/Go

**When to choose FastAPI over alternatives:**
- ✅ ML model serving (first-class async, streaming responses)
- ✅ Data ingestion APIs (high throughput, validation)
- ✅ Microservices (lightweight, fast cold starts)
- ✅ Internal tooling (auto-docs save time)
- ❌ Full admin panel needed (use Django instead)
- ❌ Simple scripts (use Flask or click/typer instead)

#### Node.js API — Express.js or Fastify

**Express.js Stack:** Express + TypeORM + PostgreSQL

**Fastify Stack:** Fastify + Prisma/Drizzle + PostgreSQL

```
When to use Node.js over Python:
- Team has strong JS/TS expertise
- Frontend is React/Next.js (shared language)
- Need existing npm ecosystem integration
```

#### Go API — Gin (RECOMMENDED)

**Stack:** Gin + GORM + PostgreSQL

**Evidence:** 88.6k stars, benchmark fastest Go framework.

```
When to use Go over Python:
- Sub-millisecond latency required
- High concurrency (10k+ requests/sec)
- Memory footprint must be minimal
- Team has Go experience
```

---

### 28.3 Full-Stack Web Applications

**RECOMMENDED Stack:**

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | Next.js 15 (App Router) | SSR/SSG, React 18, API routes |
| Styling | Tailwind CSS + shadcn/ui | Utility-first, accessible components |
| API | FastAPI (Python) or Route handlers | FastAPI for complex, Next.js for simple |
| Database | PostgreSQL | ACID, JSON, vectors, pgvector |
| Cache | Redis | Sessions, rate limiting, caching |
| Search | Typesense or Meilisearch | Typo-tolerant, fast |
| Auth | NextAuth.js or custom JWT | NextAuth for Next.js, JWT for others |
| Deploy | Vercel (frontend) + Railway/Render (backend) | Easiest scaling |

**Project Structure:**

```
web-app/
├── frontend/                 # Next.js app
│   ├── app/                # App Router pages
│   ├── components/         # UI components (shadcn/ui)
│   ├── lib/                # Utilities
│   └── public/             # Static assets
├── backend/                 # FastAPI
│   ├── src/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── core/
│   └── docker-compose.yml
├── postgres/
├── redis/
└── docker-compose.yml
```

---

### 28.4 Data Pipelines / Scraping

**Stack:** Python + FastAPI/Flask + Celery + Redis + PostgreSQL + Playwright/Scrapy

**For heavy scraping:**
```
Crawler → Playwright/Scrapy → Task Queue (Celery) → Processing (Pandas/Polars) → Database
                ↓
         Rate limiting (Redis)
         Duplicate detection (PostgreSQL)
```

**Key libraries:**
- **Scrapy** — Large-scale crawling, built-in rate limiting
- **Playwright** — JS-rendered pages, headless browsers
- **Celery** — Distributed task queue with Redis broker
- **Pandas/Polars** — Data processing (Polars for speed)
- **BeautifulSoup** — Simple HTML parsing

---

### 28.5 Machine Learning / AI Applications

**Model Serving Stack:** FastAPI + Uvicorn + PyTorch/TensorFlow

```
# Production ML serving pattern
import torch
from fastapi import FastAPI

app = FastAPI()

@app.post("/predict")
async def predict(data: InputData):
    with torch.no_grad():
        result = model(input_tensor)
    return {"prediction": result.tolist()}
```

**LLM Applications:**
- **LangChain / LlamaIndex** — RAG, agents, tool use
- **vLLM** — High-throughput LLM inference (PagedAttention)
- **pgvector** — Vector storage in PostgreSQL
- **Redis** — Semantic caching for LLM responses

**Data Processing:**
- **Polars** — Fast DataFrame library (10x pandas)
- **Dask** — Parallel pandas for out-of-memory data
- **Apache Arrow** — Columnar format for interchange

---

### 28.6 Real-Time Applications

**Stack:** Socket.io + FastAPI + Redis + PostgreSQL

```
Client ←→ Socket.io Server ←→ Redis (pub/sub) ←→ Background workers
                ↓
         FastAPI REST API (fallback)
```

**When to use WebSocket vs SSE:**
- **WebSocket (Socket.io):** Bidirectional, low latency, complex state
- **SSE (Server-Sent Events):** Server→client only, simpler, HTTP/2 friendly

**Key patterns:**
```python
# Redis pub/sub for multi-server WebSocket
# Channels: user-specific, room-specific, broadcast
```

---

### 28.7 CLI Tools

#### Python CLI — Typer (RECOMMENDED)

**Evidence:** Created by FastAPI team, 18k+ stars.

```python
import typer

app = typer.Typer()

@app.command()
def create(name: str, email: str):
    """Create a new user."""
    ...
```

**Why Typer:**
- Type hints = automatic CLI argument parsing
- Google-style docstrings = help text
- Same team as FastAPI (consistent DX)

#### Go CLI — Cobra

**Evidence:** Used by Kubernetes, Docker CLI. 35k+ stars.

**When to use:**
- Cross-compilation to multiple platforms
- Team has Go experience
- Need to integrate with Go ecosystem

---

### 28.8 Embedded / Firmware Projects

**Note:** This differs from typical software projects. See also: `/app/70d/` for Canon camera firmware example.

**Languages:**
- **C/C++** — Industry standard, maximum control
- **Rust** — Memory safety without GC, embedded support growing
- **Zig** — Emerging, systems programming with modern tooling

**When starting firmware projects:**
- Document target hardware in DEEPDIVE.md
- Track build sizes in commits
- Use QEMU for development/testing when possible

---

### 28.9 Quick Reference Table

| Project Type | Language | Framework | Database | Cache | Notes |
|-------------|----------|-----------|----------|-------|-------|
| REST API (general) | Python | FastAPI | PostgreSQL | Redis | First choice |
| REST API (high-perf) | Go | Gin | PostgreSQL | Redis | Sub-ms latency |
| REST API (Node team) | TypeScript | Express/Fastify | PostgreSQL | Redis | Team familiarity |
| Full-stack Web | TypeScript | Next.js | PostgreSQL | Redis | SSR + API routes |
| ML Model Serving | Python | FastAPI | - | Redis | Async + streaming |
| Data Pipeline | Python | FastAPI/Flask | PostgreSQL | Redis | Celery for workers |
| Real-time App | Python/TS | Socket.io | PostgreSQL | Redis | Bidirectional |
| CLI Tool | Python | Typer | - | - | Use click as alternative |
| CLI Tool | Go | Cobra | - | - | Cross-platform |
| Web Scraper | Python | Scrapy | PostgreSQL | Redis | Rate limiting built-in |
| Content Site | TypeScript | Next.js | PostgreSQL | Redis | SSG + ISR |

---

### 28.10 Tech Stack Decision Tree

When unsure what stack to choose:

```
Is it a web app with user-facing UI?
├── Yes → Next.js + Tailwind + shadcn/ui
└── No ↓

Is it an API/service?
├── Does it need ML/AI model serving?
│   ├── Yes → FastAPI + PyTorch
│   └── No ↓
├── High performance needed?
│   ├── Yes → Go/Gin or Rust/Actix
│   └── No ↓
└── Team expertise?
    ├── Python → FastAPI
    ├── Node → Express/Fastify
    └── Go → Gin

Is it a CLI tool?
├── Python team → Typer
└── Go team → Cobra

Is it embedded/firmware?
└── C/C++ (standard) or Rust (modern)
```

---

### 28.11 Anti-Recommendations

**Avoid these (unless specific reason):**
- **Django** — Overkill for APIs, use FastAPI instead
- **Flask alone** — Use FastAPI for new projects (better async, auto-docs)
- **Mongoose** — Use Prisma/Drizzle for TypeScript (better DX)
- **MongoDB** — Use PostgreSQL for most cases (ACID, JSON support)
- **REST framework (Django)** — Use FastAPI instead
- **Express alone** — Use Fastify for new projects (faster, schema validation)

### 28.12 Database Strategy — Shared vs Per-Service

For multi-service/microservice systems, the database strategy evolves with project maturity:

```
Phase 1 — MVP / Starting Out (0→1):
  Shared PostgreSQL database.
  One schema per service (e.g., `users`, `orders`, `billing`).
  Each service connects with different credentials, scoped to its schema.
  PRO: Simple, single source of truth, easy joins, no distributed transactions.
  CON: Schema coupling — services can peek at each other's tables.
       Don't. Use schema-scoped credentials. Enforce in code review.

Phase 2 — Growing / Pre-Production (1→N):
  Shared database with strict schema isolation.
  Separate schemas with per-schema users who can only see their own tables.
  Start tracking cross-service query patterns — these become future service APIs.
  Add read replicas if read volume exceeds write volume.

Phase 3 — Production / Scale:
  Database per critical service.
  Services that need independent scaling, different backup schedules,
  or different storage engines get their own database instances.
  Services that are tightly coupled and always deployed together
  can share a database instance (with separate schemas).
  NEVER split a database that requires distributed transactions
  across services without first refactoring to event-driven patterns.
```

**Rules:**
- **Start with one database.** Do not create 5 databases for a 2-developer MVP. The operational burden exceeds the isolation benefit.
- **Schema per service from day one.** `users` schema, `orders` schema, `billing` schema. Never mix service tables in the same schema. This makes the eventual split trivial — just move the schema to a new instance.
- **Schema-scoped credentials from day one.** The `orders` service connects as `orders_user` who can only see `orders.*`. This prevents accidental cross-service table access.
- **Split when you have a measurable reason, not because a blog post said so.** Valid triggers: (a) service needs different backup/restore schedule, (b) service needs different storage engine or instance size, (c) service needs independent horizontal scaling, (d) service needs different geographic deployment.
- **Never split for "architecture purity."** If two services always deploy together, always scale together, and have the same availability requirements, they can share a database instance without shame.

```python
# Phase 1 example — env config per service
# orders-service/.env
DATABASE_URL=postgresql://orders_user:pass@postgres:5432/app?options=-c%20search_path%3Dorders
#                                                            ^^^ schema-scoped

# billing-service/.env  
DATABASE_URL=postgresql://billing_user:pass@postgres:5432/app?options=-c%20search_path%3Dbilling
#                                                              ^^^ different schema
```

---

