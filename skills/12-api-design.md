# Skill 12: API Design

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 12. API Design

- **REST conventions:** `GET` (read), `POST` (create), `PATCH` (update), `DELETE` (remove)
- **Prefix:** All API endpoints use `/api/...` (no `/v1/` in the URL; version via a header or media type, with a written breaking-change policy — [Section 39](skills/39-semantic-versioning-changelog.md))
- **Response format:** Consistent wrapper `{ "data": ..., "error": null }` or `{ "items": [...], "count": N }`
- **Pagination:** Cursor-based for large datasets (opaque `cursor` + `next_cursor`), stable under inserts/deletes — offset pagination drifts
- **Error responses:** RFC 9457 Problem Details (`application/problem+json`) — `{ "type": ..., "title": ..., "status": 400, "detail": ..., "instance": ... }` instead of ad hoc error codes
- **Idempotency:** `POST`/`PATCH` accept an `Idempotency-Key` header so retries ([Section 20](skills/20-external-integrations.md)) can't create duplicates — store the key + first response and replay it
- **Rate limiting:** `429 Too Many Requests` with a `Retry-After` header (seconds) on every limited endpoint
- **Concurrency:** `ETag`/`If-Match` on mutable resources to detect lost updates; `412 Precondition Failed` on mismatch
- **Traceability:** every response carries a request ID (echo the client's or generate one) — join with logs/traces (Sections 14, 41)
- **Contract-first:** define the API as an OpenAPI spec, generate clients/servers from it, and keep the spec in the repo ([Section 48](skills/48-contract-testing-pact.md))

---

