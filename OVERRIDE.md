# OVERRIDE.md — Anchor template repository

Scope: repository-wide
Overrides: Section 5.1 — Vendored Anchor files are gitignored
Reason: This repository is the source of the Anchor template, not a project that vendors it. `AGENTS.md`, `STARTUP.md`, `routing.json`, `skills/`, and the platform configs are the product. Ignoring them would hide new sections from `git status`, silently drop them from `git add`, and exclude the deliverable from release bundles — the self-exclusion this override prevents.
Approved by: peva3 (repository owner), 2026-11-16
Review by: when this repository stops being the Anchor template source

**This file is repo-local.** It documents one repository's exception. Do not add it to the
starter bundle and do not copy it into a derived project — a derived project needs the
rule, not the exception.
