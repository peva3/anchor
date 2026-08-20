# Skill 20: External Integrations

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 20. External Integrations

For each external API/service integrated:
- **Rate limits.** Document limits and how you handle them (respect `Retry-After` / `429` / `503`; back off exponentially with jitter on `5xx`)
- **Auth method.** Document authentication mechanism (OIDC/short-lived tokens preferred; see [Section 44](skills/44-secrets-management.md))
- **Error handling.** Document error codes and retry strategy
- **Timeouts.** Every outbound call MUST have a connect and read/write timeout — never a bare client with no timeout ([Section 18](skills/18-performance-considerations.md))
- **Idempotency keys.** For retryable side-effecting calls, send an `Idempotency-Key` (Stripe pattern) so a retry can't create duplicates; never retry a non-idempotent write blindly
- **Health checks.** How to verify the integration is working
- **Webhooks.** Verify inbound webhook signatures (HMAC), include timestamp + replay protection, and respond quickly with `202` before doing work
- **SSRF hardening.** For outbound URLs derived from user input, block link-local/private addresses (169.254.169.254, 10/8, 127/8) and DNS rebinding
- **Credential rotation.** Schedule key rotation and make creds retrievable from a secret manager, not checked in (Sections 31, 44)

---

