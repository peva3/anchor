# Skill 14: Logging Standards

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 14. Logging Standards

```python
import logging
logger = logging.getLogger(__name__)

# Use lazy %s formatting (not f-strings) — f-strings evaluate eagerly even
# when the log line is discarded below the level
logger.debug("Processing item %s", item_id)
logger.info("Fetched %d items from %s", count, source)
logger.warning("Retrying after %ds", delay)
logger.error("Failed to process %s: %s", item_id, str(e))
logger.exception("Handler crashed")  # logs traceback at ERROR in an except block
```

- Use appropriate log levels: DEBUG (per-request details), INFO (operations), WARNING (recoverable issues), ERROR (failures)
- No `print` statements — use `logging`
- Include relevant context (IDs, counts, durations) in log messages
- **JSON structured logging in production:** emit one JSON object per line (`{"ts", "level", "logger", "msg", "trace_id", "service"}`) so logs are machine-queryable — `python-json-logger` or OTel bridge ([Section 41](skills/41-observability-standards.md))
- **Correlation IDs:** log the request/trace ID on every line so a single user action is joinable across services (W3C traceparent, Sections 12/41)
- **NEVER log secrets, PII, or request/response bodies verbatim** — redact auth headers, passwords, tokens, email addresses, and payloads ([Section 44](skills/44-secrets-management.md), 36.9)

---

