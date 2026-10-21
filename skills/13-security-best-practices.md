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
- **Least privilege.** Request the narrowest scopes, permissions, and host access the feature actually needs — extra permissions widen the blast radius and, for browser extensions, trigger store review
- **Output encoding.** Encode on output for the target context (HTML, attribute, URL, JS) — never build markup by concatenation
- **No dynamic code from strings.** Avoid `eval`/`new Function`/inline scripts; set a Content-Security-Policy and keep it strict
- **Validate outbound URLs.** Treat user-supplied URLs as untrusted (SSRF): allowlist schemes and hosts, and block private/loopback/metadata address ranges

---

