# Skill 58: Supply-Chain Security & SBOM

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 58. Supply-Chain Security & SBOM

Modern software is mostly dependencies. The supply chain — registry packages, base images, CI actions, build tooling — is a first-class attack surface (SolarWinds, xz-utils, left-pad). Treat it as such.

### 58.1 Dependency Verification

- **Never `curl | bash` or install dependencies fetched from unverified URLs** ([Section 36.9](skills/36-explicit-prohibitions-the-never-list.md)).
- Install from official registries only (PyPI, npm, crates.io, Maven Central, Docker Hub official images), and pin:
  - **Python**: broad constraints in `pyproject.toml` + committed `uv.lock`/`poetry.lock` + optional `--require-hashes` ([Section 17](skills/17-dependency-management.md))
  - **npm**: `package-lock.json` / `pnpm-lock.yaml` committed
  - **Images**: pin base images by **digest** (`alpine@sha256:...`), not just tag ([Section 32](skills/32-docker-support.md))
- Enable automated updates (Dependabot / Renovate) for both dependencies and GitHub Actions; review and merge, don't disable.

### 58.2 Scanning in CI

- **SCA (software composition analysis)**: `pip-audit` (free, PyPA), `osv-scanner`, `npm audit`, Trivy — run per PR, fail on HIGH/CRITICAL ([Section 31](skills/31-production-security-patterns.md), [Section 38.5](skills/38-ci-cd-pipeline-standards.md)).
- **Secret scanning**: gitleaks / GitHub secret scanning + push protection ([Section 37](skills/37-pre-commit-hook-standards.md), [Section 44](skills/44-secrets-management.md)).
- **Action pinning**: pin GitHub Actions by SHA (`uses: actions/checkout@<sha>`) and verify the SHA against the tag before adopting ([Section 38.4](skills/38-ci-cd-pipeline-standards.md)). Mutable tags (`@main`, `@v1`) are a supply-chain risk.
- **Dependency review**: enable GitHub Dependency Review on PRs to flag new vulnerable or malicious packages.

### 58.3 SBOM Generation

- Generate an SBOM at build time and attach it to each release:
  - `syft . -o spdx-json > sbom.json`
  - `trivy image --format spdx-json --output sbom.json <image>`
- Publish the SBOM alongside the artifact; link it in the release notes ([Section 39](skills/39-semantic-versioning-changelog.md)).
- Regenerate per release — a stale SBOM is misleading.

### 58.4 Signing & Provenance

- **SLSA**: aim for a provenance level that proves "built from known source, unchanged" — build in CI, record the git SHA, generate provenance (SLSA framework, `slsa-framework/slsa-github-actions`).
- **Sign artifacts**: `cosign sign` container images; sign git tags with `git tag -s` ([Section 39](skills/39-semantic-versioning-changelog.md)).
- **sigstore**: use sigstore/cosign for keyless signing tied to the CI identity, and verify signatures on ingest.
- Consumers should verify signatures + provenance before deploying, not just checksums.

### 58.5 Base Images & Build Reproducibility

- Use minimal, maintained base images; scan them (Trivy) before use.
- Prefer multi-stage builds so the runtime image carries only the app + runtime, not the build toolchain ([Section 32](skills/32-docker-support.md)).
- Keep `FROM` digests fresh via a scheduled scan/update loop; pinning forever is also a risk (known vulns accumulate).

### 58.6 Supply-Chain Rules (NEVER list additions)

- **NEVER** commit lockfiles from an unverified source or hand-edit a lockfile to "fix" a resolution.
- **NEVER** run CI actions from unknown publishers without auditing the pinned SHA and the repo.
- **NEVER** ignore HIGH/CRITICAL findings "just for now" — record a ticket and a deadline.
- **NEVER** download a dependency from a personal fork/gist when the official package exists ([Section 24.6](skills/24-common-failure-modes.md) hallucinated deps).

---

## References

- SLSA — https://slsa.dev/
- Docker best practices (pin base image digests) — https://docs.docker.com/build/building/best-practices/
- GitHub Actions security (SHA pinning) — https://docs.github.com/en/actions/reference/security/secure-use
