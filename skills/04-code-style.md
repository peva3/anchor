# Skill 04: Code Style

> Part of the Anchor skills library. Full rule text extracted from AGENTS.md.
> This is a lazy-loaded skill — load it when the corresponding task applies.
> If this skill references another section, load that section's skill file too (the referenced file is NOT included).

## 4. Code Style

### Python
- **Formatting:** PEP 8, 4-space indentation; set `line-length` explicitly in `[tool.ruff]`/`[tool.black]` (default 88, 100 is fine if configured) — pick one and configure it so ruff format and the style guide agree
- **Naming:** `snake_case` (variables/functions), `PascalCase` (classes), `SCREAMING_SNAKE` (constants)
- **Imports:** Grouped stdlib → third-party → local; alphabetical within groups
- **Types:** Use type hints for all function signatures. Modern syntax (Python 3.9+): builtin generics `list[str]`, `dict[str, int]` (PEP 585); unions `int | None` (PEP 604); `Self` for class methods; `match/case` (PEP 634) over long if/elif chains; dataclasses over hand-written `__init__`
- **Strings:** f-strings for interpolation (not `%` or `.format()`)
- **Docstrings:** Google style for modules, classes, and public functions
- **Error Handling:** Specific exceptions, never bare `except:`
- **Async:** Use `async/await` for I/O-bound operations

### TypeScript / JavaScript
- **Formatting:** 2-space indentation; pin semicolons and style with ESLint/Prettier or Biome (don't leave it "optional")
- **Naming:** `camelCase` (variables/functions), `PascalCase` (components/types)
- **Types:** `tsc --noEmit` in CI, strict mode enabled, explicit return types on exported functions
- **Components:** Functional components with hooks, no class components

### General
- No emojis in code or commit messages
- No `print` statements — use `logging`
- Keep functions under 50 lines; extract sub-functions for complex logic
- Add tests for all new functionality

### Language — English Only
- **ALL code, comments, documentation, variable names, commit messages, and user-facing text MUST be in English**
- No foreign language in any file, variable name, comment, or documentation
- This ensures all agents and developers across any language background can collaborate effectively
- Exception: Test data with realistic content (names, addresses) may use any language for authenticity

---

