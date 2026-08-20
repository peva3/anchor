# Skill 02: Commit Protocol

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 2. Commit Protocol

**After completing and verifying any task:**
1. `git add <changed files>`
2. `git commit -m "Descriptive commit message"` — describe WHAT changed and WHY
3. `git push origin <branch>`

**GitHub automation (if `gh` command is available):**
- If the user has explicitly approved a commit and push, you may run them after validation
- Only commit/push when a LOGICAL UNIT OF WORK IS COMPLETE — never commit halfway through a feature, in the middle of debugging, or with known-broken state
- Each commit should be a stable checkpoint that passes all tests independently
- Use `gh auth status` to verify auth before attempting pushes
- If `gh` is logged in, push to the user's remote using their configured identity
- **NEVER** create GitHub Actions workflows, dependabot config, or any other GitHub-side automation without explicit per-file user approval — see Section 36.4a
- **NEVER** create PRs, issues, or comments without explicit user approval (see "Never Go Rogue" below)

**IMPORTANT — Never Go Rogue:**
- **NEVER** create PRs, issues, comments, or any GitHub activity without **explicit user approval**
- The agent must wait for the user to explicitly request: "yes, create the PR", "yes, post that comment", etc.
- Exception: The user explicitly authorizes automated commits/pushes (which is covered above)
- When in doubt, ask first

**IMPORTANT — Never Spend Money:**
- **NEVER** create GitHub Actions workflows that use paid runners, consume API credits, or incur any financial cost without explicit user approval
- **NEVER** enable GitHub features that trigger billing (GitHub Actions with large runners, GitHub Packages storage beyond free tier, Codespaces beyond free limits, GitHub Copilot for business, etc.)
- **NEVER** sign up for paid services, create cloud resources, provision API keys with billing, or do anything that could generate a financial charge
- **NEVER** modify billing settings, change plan tiers, or enable paid add-ons
- **NEVER** create CI/CD workflows that call paid third-party APIs without confirmation
- When in doubt — if an action involves any external service that might cost money — **ask first**

**IMPORTANT — Always Use the User's Identity:**
- **ALWAYS** use the configured author identity for ALL GitHub activity — commits, PRs, issues, comments, and any content attributed to a person
- **NEVER** impersonate, use a different username, create a separate bot account, or sign commits as anyone other than the configured identity
- **NEVER** attribute work to "the AI" or "the agent" in commit messages, PR descriptions, or comments — all work is attributed to the human author
- **NEVER** claim the agent wrote something independent of the user's direction
- The configured identity is the single source of truth for who authored all changes

**Author identity (already configured globally):**
- The agent should use the user's globally configured git identity for all commits
- Never change git config `user.name` or `user.email` — use what is already set
- Verify identity with `git config --global user.name` and `git config --global user.email` before first commit

**Message format conventions:**
- Prefix with scope when applicable: `api: add rate limiting`, `frontend: fix timeline scroll bug`
- For TODO completions: `Sprint N: <description>`
- Include size delta for binary builds: `autoexec.bin +12KB`

---

