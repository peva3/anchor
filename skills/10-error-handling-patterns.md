# Skill 10: Error Handling Patterns

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 10. Error Handling Patterns

```python
# Good: specific exception with context
try:
    result = await client.post(url, json=data)
    result.raise_for_status()
except httpx.TimeoutException:
    logger.warning(f"Timeout calling {model}, retrying")
    raise RetryableError(f"Timeout for {url}") from None
except httpx.HTTPStatusError as e:
    logger.error(f"HTTP {e.response.status_code} from {url}")
    raise ApiError(f"Failed to call {url}") from e

# Bad: silent swallow
except Exception:
    pass
```

- Always include context in exceptions; use `raise ... from e` to preserve the original traceback (PEP 3134). Use `from None` only when the cause is deliberate noise (e.g. a timeout being re-raised as a retryable error) and you want to suppress the chain
- For concurrent failure, Python 3.11+ raises `ExceptionGroup` (PEP 654) from `asyncio.gather`/`TaskGroup` — catch with `except*` or use `cancel_scope`/`TaskGroup` results, don't let the group crash the app
- In handlers, use `logger.exception(...)` inside the `except` block to capture the traceback
- Log at appropriate level: DEBUG for retryable, WARNING for degraded, ERROR for fatal
- Use `None` return with type annotation, not tuple

---

