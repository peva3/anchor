# Skill 18: Performance Considerations

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 18. Performance Considerations

- **Async for I/O.** Use `asyncio` and `httpx.AsyncClient` for concurrent HTTP calls
- **NEVER block the event loop.** Sync I/O (files, `requests`, `time.sleep`, CPU-bound loops) inside a coroutine stalls every concurrent task — offload with `asyncio.to_thread` / `loop.run_in_executor` / `run_in_process`, or use async-native libs
- **Connection pooling.** Reuse HTTP clients and database connections
- **Caching.** Cache expensive operations with appropriate TTLs — and define cache invalidation (keyed on the inputs; never serve stale for mutable reads without a version check)
- **Batching.** Batch API calls and DB writes where possible; watch for the **N+1 query** anti-pattern (per-row queries in a loop — [Section 27](skills/27-code-quality-standards.md)) — fetch related rows in one query
- **Profile before optimizing.** Use `cProfile` (Python) or `py-spy` (attach to a running process), not guesses — optimize the measured bottleneck
- **Size checks.** Optimize what the profile proves hot; don't micro-optimize cold paths ([Section 50](skills/50-intentional-minimalism-the-simplicity-first-architecture.md))

---

