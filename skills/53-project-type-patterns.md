# Skill 53: Project Type Patterns

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.

## 53. Project Type Patterns

AGENTS.md was originally web-service and Python-focused. This section extends coverage to five common non-web project types with language-agnostic patterns that apply regardless of stack.

### 53.1 Mobile Apps (iOS / Android / React Native)

Mobile projects have unique constraints: app store review cycles, platform-specific permissions, offline behavior, and strict size budgets.

**Platform-specific testing:**
```
iOS:         XCTest (unit), XCUITest (UI), Detox (E2E)
Android:     JUnit (unit), Espresso (UI), Maestro (E2E)
React Native: Jest (unit), Detox (E2E), Maestro (E2E)
```

**Push notifications:**
- Register for push permissions at first meaningful interaction, not on app launch
- Handle token refresh — store tokens server-side, not just in memory
- Test silent pushes (background) vs user-visible pushes separately
- Never rely on push delivery timing — treat as best-effort

**Offline behavior:**
- Every network call must have an offline fallback (cached data, empty state, or error)
- Use local storage (SQLite, Core Data, Room) as source of truth, sync to server
- Test with airplane mode, throttled networks, and intermittent connectivity
- Never show a spinner that never resolves — always have a timeout with user-visible state

**Mobile permissions:**
- Request permissions at the moment of use, not at app launch (iOS requirement)
- Handle "denied" state gracefully — show in-app explanation, link to settings
- Test the "previously denied" flow, not just the "first time" flow

**Crash reporting:**
```
Sentry       — Cross-platform, source maps, breadcrumbs
Crashlytics  — Firebase integration, free tier
Bugsnag      — Real-time alerts, release tracking
```
- Every release must have crash reporting enabled before app store submission
- Include user context (user ID, session ID) in crash reports
- Never log PII in crash breadcrumbs

**App size budget:**
- iOS: App Store limit is 200MB over cellular; aim for <100MB
- Android: Google Play limit is 150MB; aim for <50MB
- Track size per release in CI — fail the build if size regresses >5%
- Use App Thinning (iOS) / App Bundle (Android) to reduce per-device size

**E2E mobile testing:**
```
Device farms: BrowserStack, Sauce Labs, AWS Device Farm
Local:       Maestro (fast, YAML-based), Detox (JS-native)
```
- Run E2E on at least 2 iOS devices (small + large) and 2 Android devices
- Never rely solely on simulators — test on real devices at least weekly

### 53.2 Embedded Firmware (C / C++ / Rust)

Embedded projects have no internet, no Docker, no cloud. Code must be deterministic and resource-constrained.

**Cross-compilation toolchain:**
```
ARM Cortex-M:  arm-none-eabi-gcc (GNU ARM Embedded Toolchain)
RISC-V:        riscv32-unknown-elf-gcc / riscv64-unknown-elf-gcc
ESP32:         xtensa-esp32-elf-gcc (ESP-IDF)
STM32:         arm-none-eabi-gcc + STM32CubeIDE
```
- Pin toolchain version in CI (e.g., `gcc-arm-none-eabi-10.3-2021.10`)
- Document toolchain installation in README — never assume developer has it
- Use `CMake` or `Make` for build system; avoid IDE-specific project files

**Static analysis for C/C++:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pocc/pre-commit-hooks
    rev: v1.3.5
    hooks:
      - id: cppcheck
        args: [--enable=all, --suppress=missingIncludeSystem]
      - id: clang-tidy
        args: [-p, build/]
      - id: clang-format
        args: [-i, --style=file]
```
- Run `cppcheck --enable=all` on every commit
- Use `clang-tidy` with MISRA-C or CERT-C rules for safety-critical code
- Use `clang-format` with a `.clang-format` file for consistent style

**Code formatting:**
```yaml
# .clang-format
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
AllowShortFunctionsOnASingleLine: Inline
```
- Commit `.clang-format` to the repo root
- Run `clang-format -i *.c *.h` in pre-commit hooks

**Interrupt handler discipline:**
- ISRs must be short — set a flag, copy data, return immediately
- Never call `malloc`, `printf`, or blocking functions from an ISR
- Use atomic operations or disable interrupts for shared state access
- Document every ISR with: trigger source, max execution time, shared state

**Flash/ROM size tracking:**
```bash
# Track binary size in CI
arm-none-eabi-size build/firmware.elf
# text    data     bss     dec     hex filename
# 45232   1024    2048   48304    bcb0 build/firmware.elf
```
- Fail CI if text+data exceeds 90% of available flash
- Track size delta per PR — alert if a PR adds >1KB without justification

**OTA / firmware update:**
- Implement dual-bank flash layout (active + staging)
- Verify firmware signature before applying update
- Implement rollback on boot failure (watchdog timer)
- Never OTA-update without a verified rollback path

### 53.3 Data Pipelines / ETL

Data pipelines must be idempotent, resumable, and observable. Failures are inevitable — the system must recover gracefully.

**Idempotency:**
- Every task must produce the same output when run twice with the same input
- Use `UPSERT` (INSERT ON CONFLICT UPDATE) instead of INSERT for writes
- Include `run_id` or `execution_date` in output to enable deduplication
- Never append to a table without a deduplication step

**Backfill procedure:**
```python
# Airflow backfill example
from airflow.utils.dates import days_ago

# Backfill last 30 days
for dt in days_ago(30).to_datetime_range(end_date=days_ago(0)):
    dag_run = dag.create_dagrun(
        execution_date=dt,
        state=State.QUEUED,
        run_type=DagRunType.MANUAL,
    )
```
- Always backfill in chronological order (oldest first)
- Verify data quality after backfill before marking complete
- Document backfill ranges in DEEPDIVE.md for audit trail

**Schema evolution:**
- Use a schema registry (Confluent Schema Registry, AWS Glue) for Avro/Protobuf
- For SQL: use migration tools (Alembic, Flyway) with backward-compatible changes
- Never drop a column that downstream consumers might still read
- Add new columns as NULLABLE, backfill, then add NOT NULL constraint

**DAG/task testing:**
```python
# Airflow task test
def test_extract_task():
    """Test that extract task produces expected output."""
    dag = create_dag()
    task = dag.get_task('extract_users')
    
    # Mock external API
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = sample_data
        result = task.execute(context={})
    
    assert len(result) == 100
    assert all('email' in row for row in result)
```
- Test every task in isolation with mocked dependencies
- Test DAG structure (no cycles, correct dependencies) with `dag.test()`
- Test end-to-end with a small sample dataset in CI

**Data quality checks:**
```python
# Great Expectations example
import great_expectations as ge

df = ge.read_csv('users.csv')
df.expect_column_values_to_be_unique('user_id')
df.expect_column_values_to_be_between('age', 0, 150)
df.expect_column_values_to_match_regex('email', r'^[\w\.-]+@[\w\.-]+\.\w+$')
```
- Run data quality checks after every load, before downstream tasks
- Quarantine bad records to a `dead_letter` table, don't fail the pipeline
- Alert on data quality regression (e.g., null rate increases >5%)

### 53.4 CLI Tools

CLI tools must be installable, discoverable, and predictable. Exit codes and output formats are part of the API.

**CLI argument design:**
```python
# Typer (Python) — recommended for new projects
import typer

app = typer.Typer()

@app.command()
def process(
    input_file: Path = typer.Argument(..., help="Input file path"),
    output: Path = typer.Option(None, "--output", "-o", help="Output file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """Process input file and write results."""
    ...
```
- Use `--long-name` for all options, `-s` short aliases for common ones
- Every option must have a `help` string
- Use `typer.Argument` for required positional args, `typer.Option` for flags

**Exit codes:**
| Code | Meaning | When to Use |
|------|---------|-------------|
| 0 | Success | Command completed successfully |
| 1 | General error | Unspecified failure |
| 2 | Misuse of command | Invalid arguments, missing required options |
| 126 | Permission denied | File not executable, access denied |
| 127 | Command not found | Subcommand doesn't exist |
| 130 | Interrupted | User pressed Ctrl+C |

**stdout vs stderr discipline:**
- Write machine-readable output to `stdout` (JSON, CSV, plain text)
- Write human-readable messages (progress, warnings, errors) to `stderr`
- Never mix machine output and human messages on the same stream
- Use `--quiet` flag to suppress human messages, `--json` for machine output

**Shell completion:**
```bash
# Generate completion scripts
typer mycli utils completion --install
# Or manually:
mycli --show-completion bash > /etc/bash_completion.d/mycli
```
- Generate completion scripts for bash, zsh, fish, PowerShell
- Include completion installation in README
- Test completion in CI with `complete -p mycli`

**Distribution:**
```toml
# pyproject.toml
[project.scripts]
mycli = "mycli.main:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```
- Publish to PyPI (Python) or npm (Node.js) with semantic versioning
- Include `CHANGELOG.md` with every release
- Sign releases with GPG for security-sensitive tools

**Man pages / docs generation:**
```bash
# Generate man pages from Typer CLI
typer mycli utils docs --name mycli --output docs/man/
# Or use cobra (Go)
cobra-cli gen-docs --dir docs/
```
- Generate man pages and HTML docs from CLI definitions
- Include `--help` output in README
- Keep docs in sync with code — regenerate on every release

### 53.5 Static Sites / Documentation

Static sites have no backend, no database. Content is the product. SEO, accessibility, and link integrity are critical.

**Static site generator choice:**
```
Jekyll      — Ruby, GitHub Pages native, simple blogs
Hugo        — Go, fastest build times, large sites
MkDocs      — Python, technical documentation, Material theme
Docusaurus  — React, versioned docs, i18n, Facebook
Astro       — JavaScript, content-focused, islands architecture
```

**Content versioning:**
```yaml
# MkDocs mike (versioned docs)
mike deploy --push --update-aliases 1.0 latest
mike set-default --push latest
```
- Use `mike` (MkDocs) or Docusaurus versioning for multi-version docs
- Keep `latest` alias pointing to most recent stable release
- Never delete old versions — archive them

**Documentation search:**
```
Algolia DocSearch  — Free for open source, hosted
Lunr.js            — Client-side, no server needed
Meilisearch        — Self-hosted, typo-tolerant
```
- Enable search on every documentation site
- Index all pages including API reference
- Test search with common queries (installation, quickstart, troubleshooting)

**SEO meta tags:**
```html
<!-- Every page must have these -->
<title>Page Title — Site Name</title>
<meta name="description" content="150-160 character description">
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Description">
<meta property="og:image" content="https://example.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://example.com/page-url">
```
- Every page must have unique title, description, og:image
- Use canonical URLs to prevent duplicate content
- Validate with Google Search Console after deployment

**Link checking:**
```yaml
# CI link check
- name: Check links
  run: |
    pip install htmlproofer
    htmlproofer ./_site --check-html --check-external-hash
```
- Run link checker in CI on every PR
- Check internal links, external links, and image references
- Fail the build on broken links

**Multi-language support (i18n):**
```yaml
# MkDocs i18n config
plugins:
  - i18n:
      default_language: en
      languages:
        en: English
        es: Español
        fr: Français
```
- Use `i18n` plugin (MkDocs) or Docusaurus i18n for multi-language docs
- Translate navigation, not just content
- Use professional translation services for user-facing docs, not machine translation

**Preview deployments:**
```yaml
# Netlify preview (netlify.toml)
[build]
  publish = "_site"
  command = "jekyll build"

# Vercel preview (vercel.json)
{
  "github": {
    "silent": true
  }
}
```
- Enable PR previews on Netlify, Vercel, or Cloudflare Pages
- Post preview URL as PR comment automatically
- Never merge without reviewing the preview deployment

### 53.6 Language-Agnostic Patterns

These patterns apply regardless of programming language.

**Java / Kotlin:**
```
Build:       Maven or Gradle (Gradle preferred for new projects)
Testing:     JUnit 5 + Mockito (unit), Testcontainers (integration)
Formatting:  Google Java Format or ktlint (Kotlin)
Static:      SpotBugs, Error Prone, detekt (Kotlin)
```
- Use `mvn verify` or `./gradlew check` in CI
- Enforce code style with `spotless` plugin
- Use `@Nullable` / `@NonNull` annotations for null safety

**Swift:**
```
Build:       Xcode or Swift Package Manager
Testing:     XCTest (unit), XCUITest (UI)
Formatting:  SwiftFormat
Static:      SwiftLint
```
- Use `swift test` in CI for SPM projects
- Enforce SwiftLint rules in pre-commit hooks
- Use `async/await` for concurrency (Swift 5.5+)

**Rust:**
```
Build:       cargo
Testing:     cargo test (unit + integration), proptest (property-based)
Formatting:  rustfmt
Static:      clippy (mandatory)
```
- Run `cargo clippy -- -D warnings` in CI — treat warnings as errors
- Use `cargo fmt --check` in pre-commit hooks
- Use `#[must_use]` on functions returning `Result` or `Option`

**C / C++:**
```
Build:       CMake or Make
Testing:     Google Test (C++), Unity (C)
Formatting:  clang-format
Static:      cppcheck, clang-tidy, Coverity
```
- Use `cmake --build . --target test` in CI
- Enforce MISRA-C or CERT-C for safety-critical code
- Use AddressSanitizer and UndefinedBehaviorSanitizer in CI

### 53.7 Template Coverage and Out-of-Scope

This template is **best suited for:**
- Web services (REST APIs, full-stack apps)
- Python projects (FastAPI, Django, Flask)
- JavaScript/TypeScript projects (Node.js, React, Next.js)
- Go projects (Gin, Echo)
- Microservices architectures
- Cloud-native deployments (Docker, Kubernetes)

**Partial coverage** (use this template as a foundation, add domain-specific sections):
- CLI tools (Section 53.4 covers basics)
- Embedded firmware (Section 53.2 covers basics)
- Data pipelines (Section 53.3 covers basics)
- Static sites (Section 53.5 covers basics)
- Mobile apps (Section 53.1 covers basics)

**Out of scope** (not covered by this template):
- Game development (Unity, Unreal, Godot)
- Browser extensions (Chrome, Firefox, Safari)
- Desktop applications (Electron, Tauri, native)
- Blockchain / smart contracts (Solidity, Rust on Solana)
- Hardware design (PCB layout, FPGA)
- Scientific computing (MATLAB, R, Julia)

**When to extend this template:**
If your project type is "partial coverage" or "out of scope," create a `docs/PROJECT_TYPE_EXTENSION.md` file that adds domain-specific patterns. Reference this AGENTS.md as the foundation and extend with project-type-specific rules.

---

