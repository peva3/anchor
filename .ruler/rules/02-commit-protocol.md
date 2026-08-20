# 02-commit-protocol.md

## After Completing Any Task
1. `git add <files>` — add specific files, never `git add .` (Section 36.2)
2. `git commit -m "...` — human-sounding, WHY-focused message
3. `git push origin <branch>`

## Never Go Rogue
- NEVER create PRs, issues, or comments without explicit user approval
- Wait for explicit "yes, create the PR" before any GitHub activity

## Never Spend Money
- NEVER create paid-runner workflows, enable billing, sign up for paid services
- When in doubt — if an action could cost money — ask first

## No GitHub-Side Automation (Section 36.4a)
- NEVER create GitHub Actions workflows, dependabot config, or bot PRs without explicit per-file user approval

## Always Use User Identity
- Use globally configured git identity for all commits and activity
- NEVER impersonate, use bot accounts, or attribute work to AI

[Source: AGENTS.md Section 2; cross-references Section 36.2, 36.4a]
