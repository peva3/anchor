# Skill 18: Performance Considerations

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 18. Performance Considerations

- **Async for I/O.** Use `asyncio` and `httpx.AsyncClient` for concurrent HTTP calls
- **Connection pooling.** Reuse HTTP clients and database connections
- **Caching.** Cache expensive operations with appropriate TTLs
- **Batching.** Batch API calls and DB writes where possible
- **Profile before optimizing.** Use profiling tools to identify bottlenecks, don't guess

---

