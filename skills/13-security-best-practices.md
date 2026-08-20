# Skill 13: Security Best Practices

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 13. Security Best Practices

- **Input validation.** Use Pydantic models or equivalent for all API inputs
- **Parameterized queries.** Never use string interpolation for SQL
- **Sanitize for logging.** Use `sanitize_for_logging()` before logging user input
- **Redact secrets.** API keys masked in logs automatically
- **Rate limiting.** Implement on public endpoints
- **No secrets in code.** All secrets via env vars or mounted secrets

---

