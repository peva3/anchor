# LangChain AGENTS.md

Source: https://raw.githubusercontent.com/langchain-ai/langchain/master/AGENTS.md

## Overview

Global development guidelines for the LangChain Python monorepo - a comprehensive framework for building agents and LLM-powered applications.

## Key Sections Found

### Project Architecture
- Monorepo structure with multiple packages
- Core layer (langchain-core) - base abstractions
- Implementation layer (langchain-classic)
- Partner integrations layer
- Testing layer (standard-tests)

### Development Tools
- `uv` - Fast Python package manager
- `make` - Task runner
- `ruff` - Linter and formatter
- `mypy` - Static type checking
- `pytest` - Testing framework

### Environment Management
- Use `uv` for all dependency operations
- Never use pip/poetry/conda directly
- Editable installs for local development
- Package-specific Python version targets

### Code Quality Standards
- Type hints and return types REQUIRED
- Google-style docstrings
- Descriptive variable names
- Break up complex functions (>20 lines)
- Never use eval(), exec(), pickle on user input

### Testing Requirements
- Unit tests: `tests/unit_tests/` (no network)
- Integration tests: `tests/integration_tests/` (network ok)
- Every feature/bugfix MUST have tests
- Mirror source structure in tests
- Tests fail when logic is broken

### Documentation Standards
- Google-style docstrings
- American English spelling
- Single backticks for code references
- Focus on "why" not "what"

### PR and Commit Guidelines
- Conventional Commits format
- Scope required in title
- Lowercase after scope unless proper noun
- Short, descriptive titles

### Branch Naming
- `<github-username>/<scope>/<short-description>`
- Kebab-case description

### Key Insights for AGENTS.md

1. **Explicit tool requirements** - make, uv, ruff, mypy specified
2. **Command examples** - Actual commands to run
3. **PR title format** - Clear conventions with examples
4. **Breaking change warnings** - Critical for API stability
5. **Type hints mandatory** - Enforced standard
6. **Test coverage requirement** - Every feature needs tests
7. **Docstring style** - Google-style with examples
8. **Security considerations** - No eval/exec/pickle