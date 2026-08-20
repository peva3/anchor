# Skill 05: Project Structure Conventions

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 5. Project Structure Conventions

```
project/
├── src/                    # Source code
│   ├── api/               # API routes/endpoints
│   ├── models/            # Data models/schemas
│   ├── services/          # Business logic
│   └── core/              # Config, logging, exceptions
├── tests/                  # All tests, one-off scripts, random tooling
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── scripts/           # Random scripts (gitignored)
├── docs/                  # Architecture docs, ADRs, runbooks
├── research/              # Research files, whitepapers, references
├── scripts/               # CLI/tools (version controlled)
├── docker/                # Dockerfiles, compose
├── DEEPDIVE.md            # System narrative — detailed explanation
├── .env.example           # Environment template
├── .gitignore             # Git ignore (ALWAYS includes tests/)
├── README.md              # Setup and usage
├── AGENTS.md              # This file
└── TODO.md                # Task tracking
```

**Required folders for every new project:** `tests/`, `docs/`, `research/`

**DEEPDIVE.md — Living System Narrative:**

Every project MUST have a `DEEPDIVE.md` file at the root. This is not documentation — it's a detailed narrative explaining HOW and WHY the system is built the way it is.

**When to update DEEPDIVE.md:**
- After ANY architectural change
- After ANY significant refactor
- When adding new integration patterns
- When removing code (explain WHY it was removed)
- When making decisions that future agents need to understand

**DEEPDIVE.md must cover:**
- **System layout** — Why files are organized this way, why this tech stack
- **Data flow** — How data moves through the system, from ingestion to output
- **Key decisions** — Every non-obvious choice, including alternatives rejected and WHY
- **Gotchas and landmines** — Known failure modes, edge cases that bite
- **Interconnections** — How services/Modules communicate, what depends on what
- **Why things work** — Not just WHAT the code does, but WHY it was designed that way

**DEEPDIVE.md is NOT:**
- A substitute for inline comments
- A restatement of what code does (assume the code is self-documenting)
- Static — it MUST be updated when the system changes

**Example DEEPDIVE.md entry:**
```markdown
## Why the API is Split into public/admin

We split the API into port 8000 (public, read-only+search) and port 8004 
(admin, localhost-only, full CRUD) because:

- The ingestion pipeline needs to write without auth overhead
- Admin operations (scraper config, manual overrides) shouldn't be exposed
- Public users only need search and read operations
- This follows defense-in-depth: even if public API is compromised,
  admin operations remain protected by network isolation

Date: 2026-05-15
Decision: Split API into dual ports (migration 009)
```

---

