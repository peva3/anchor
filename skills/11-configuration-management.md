# Skill 11: Configuration Management

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 11. Configuration Management

- **Environment variables** for all configurable values (12-Factor: config in the environment, not in code)
- **`.env.example`** as a template with all variables documented; `.env` itself is NEVER committed ([Section 44](skills/44-secrets-management.md))
- **Prefix convention** for namespacing (e.g., `APP_`, `SERVICE_`, `DB_`)
- **No config files in code** — everything via env vars or `.env`
- **Validate at startup (fail fast):** parse and validate all config before serving traffic, so a missing/mistyped var fails loudly at boot, not mid-request. Use `pydantic-settings` (Python) or an equivalent typed config loader; define types, defaults, and required flags
- **Environment precedence:** CLI/process env > `.env` file > defaults — document the order and keep it deterministic across local, CI, and prod
- **Secrets vs non-secrets:** keep secrets out of non-secret config files and out of version control entirely; reference them by name from the secret manager ([Section 44](skills/44-secrets-management.md))
- **Test the config path:** a wrong config value is a production incident — include a config smoke check in CI

---

