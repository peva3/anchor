# Skill 07: Docker / Deployment

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 7. Docker / Deployment

- **Rebuild after code changes.** Containers use built images, not source files. After modifying code:
  ```bash
  docker compose build <service> && docker compose up -d <service>
  # or for all services:
  docker compose up -d --build
  ```

- **Container health checks.** All services should have healthcheck configured.

- **Ports.** Document all exposed ports and what runs on each:
  ```
  | Service | Port | Host Access | Role |
  |---------|------|-------------|------|
  | api     | 8000 | :8000       | REST API |
  | frontend| 3000 | :3090       | Web UI   |
  ```

- **Environment variables.** Use `.env.example` with documented defaults. All config via env vars, not code changes.

---

### Image Size and Build Hygiene

- **Use a multi-stage build**: compile or install in a builder stage, copy only the artifacts into a slim runtime stage. A single-stage image ships compilers, caches, and source it does not need.
- **Pin the base image and prefer slim/distroless variants** (`python:3.12-slim`, `gcr.io/distroless/...`) rather than `latest`.
- **Add a `.dockerignore`** covering `.git`, virtualenvs, caches, test data, and secrets — otherwise they land in the build context and can end up in a layer.
- **Measure before claiming a size win**: record the image size before and after (`docker images`) and report both, per [Section 50.6](skills/50-intentional-minimalism-the-simplicity-first-architecture.md).
- **Keep layers cacheable**: copy dependency manifests and install before copying source, so code changes do not invalidate the dependency layer.
