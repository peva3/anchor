# Skill 39: Semantic Versioning & Changelog

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 39. Semantic Versioning & Changelog

### 39.1 Semantic Versioning Rules

Follow [SemVer 2.0.0](https://semver.org/) strictly:

| Version Component | Increment When | Example |
|------------------|----------------|---------|
| **MAJOR** (`X.0.0`) | Incompatible API changes | Removing an endpoint, changing response format, changing behavior of existing API |
| **MINOR** (`0.X.0`) | Backward-compatible functionality | Adding a new endpoint, adding optional parameters, deprecating with warnings |
| **PATCH** (`0.0.X`) | Backward-compatible bug fixes | Fixing a calculation error, correcting a typo in output, performance improvements with no API change |

**0.x caveat:** while a project is at `0.x`, SemVer treats MINOR as potentially breaking — use `0.x.0` for breaking changes and `0.0.x` for compatible fixes. Document this in the README so consumers know `0.2.0 → 0.3.0` may not be safe.

**Prerelease & build metadata:** use `-rc.1`, `-beta.2`, `-alpha.1` for pre-releases (lower precedence than the final release) and `+build.123` for build metadata (ignored for precedence). Example: `2.0.0-rc.1`.

**No bump for chore-only changes:** documentation, CI, or internal refactoring-only changes MUST NOT bump the version — they ride along with the next real release.

**What constitutes a "breaking change":**
- Removing an API endpoint
- Changing response field names or types
- Removing or renaming public functions/classes
- Changing the behavior of existing functionality (even if signature is the same)
- Changing default values that alter behavior
- Dropping support for a Python version
- Changing environment variable names

**What is NOT a breaking change:**
- Adding new API endpoints
- Adding optional parameters with defaults
- Adding new functions/classes
- Bug fixes that restore intended behavior
- Internal refactoring (no public API change)
- Documentation-only changes

### 39.2 Keep a Changelog Format

Use the [Keep a Changelog](https://keepachangelog.com/) format in `CHANGELOG.md`:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature A
- New feature B

### Changed
- Modified behavior of X for better Y

### Deprecated
- Feature Z will be removed in v3.0.0

### Removed
- Removed deprecated feature W

### Fixed
- Bug where X would crash on Y input

### Security
- Fixed vulnerability in authentication flow

## [1.2.0] - 2026-06-15

### Added
- Pagination support for list endpoints
- Health check endpoint with per-subsystem status

## [1.1.0] - 2026-06-01

### Added
- User authentication system

### Fixed
- Race condition in token refresh (#42)

## [1.0.0] - 2026-05-15

### Added
- Initial release
```

**Rules:**
- **Every release MUST have a CHANGELOG entry** — no exceptions
- **Entries are grouped by type:** Added, Changed, Deprecated, Removed, Fixed, Security
- **Each entry describes the change** from the USER's perspective, not the developer's
- **The [Unreleased] section** is updated as changes are merged
- **On release**, [Unreleased] is moved to a versioned section with the release date
- **Do NOT** list every commit — summarize user-visible changes
- **Do NOT** include internal refactoring, dependency updates (unless they fix security issues), or tooling changes

### 39.3 Conventional Commits for Changelog Automation

Use [Conventional Commits](https://www.conventionalcommits.org/) format for all commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types and their CHANGELOG mapping:**

| Type | CHANGELOG Section | Example |
|------|------------------|---------|
| `feat:` | Added | `feat: add pagination to search endpoint` |
| `fix:` | Fixed | `fix: prevent race condition in token refresh` |
| `docs:` | (not in changelog) | `docs: update API documentation` |
| `style:` | (not in changelog) | `style: format with ruff` |
| `refactor:` | (not in changelog) | `refactor: extract validation logic` |
| `perf:` | Changed | `perf: improve query performance 3x` |
| `test:` | (not in changelog) | `test: add edge case tests for pagination` |
| `chore:` | (not in changelog) | `chore: update dependencies` |
| `ci:` | (not in changelog) | `ci: add coverage enforcement to CI` |

**Breaking changes:**
- Add `!` after the type: `feat!: remove deprecated v1 endpoint`
- Or add `BREAKING CHANGE:` in the footer:
  ```
  feat: migrate to v2 API

  BREAKING CHANGE: The /v1/ endpoints are no longer available.
  All clients must migrate to /v2/ before upgrading.
  ```

### 39.4 Git Tags

```bash
# Create a SIGNED annotated tag (NOT lightweight) — cryptographic provenance
git tag -s v1.2.3 -m "Release v1.2.3

### Added
- Pagination support for list endpoints
- Health check endpoint with per-subsystem status

### Fixed
- Race condition in token refresh (#42)
"

# Push tags to remote
git push origin v1.2.3

# Verify tag exists and is signed
git tag -l "v*"
git tag -v v1.2.3
```

- Sign release tags with `git tag -s` (SSH/Sigstore/OpenPGP) so consumers can verify provenance.
- At release time, link the artifact's **SBOM** and checksums to the release (see the Supply-Chain Security skill) — a version tag without an SBOM is not fully auditable.

### 39.5 Release Automation

Tools for automating releases:

| Tool | When to Use | Setup Complexity |
|------|-------------|-----------------|
| **release-please** (Google) | Monorepos, conventional commits, automated CHANGELOG | Medium |
| **semantic-release** | Node.js/JS projects with conventional commits | Low |
| **Manual + script** | Small projects, infrequent releases | Low |

**Minimum release process for any project:**
1. All changes merged to main via PR
2. CI passes on main
3. Update CHANGELOG.md (move [Unreleased] to versioned section)
4. Commit: `chore: release v1.2.3`
5. Tag: `git tag -a v1.2.3 -m "Release v1.2.3"`
6. Push: `git push origin main --tags`
7. Verify release appears in GitHub Releases

---

