# LangChain Global Development Guidelines

## Monorepo Structure

LangChain is a Python monorepo with multiple independently versioned packages that use `uv`.

```
langchain/
├── libs/
│   ├── core/             # `langchain-core` primitives and base abstractions
│   ├── langchain/        # `langchain-classic` (legacy, no new features)
│   ├── langchain_v1/     # Actively maintained `langchain` package
│   ├── partners/         # Third-party integrations
│   │   ├── openai/       # OpenAI models and embeddings
│   │   ├── anthropic/    # Anthropic (Claude) integration
│   │   └── ... (other integrations)
│   ├── text-splitters/   # Document chunking utilities
│   ├── standard-tests/   # Shared test suite for integrations
│   └── model-profiles/   # Model configuration profiles
```

## Development Tools

- `uv` - Fast Python package installer and resolver
- `make` - Task runner for common development commands
- `ruff` - Fast Python linter and formatter
- `mypy` - Static type checking
- `pytest` - Testing framework

## Key Commands

```bash
# Install all groups
uv sync --all-groups

# Run unit tests
make test

# Lint code
make lint

# Format code
make format

# Type checking
uv run --group lint mypy .
```

## Code Quality Standards

- All Python code MUST include type hints and return types
- Use descriptive, self-explanatory variable names
- Follow existing patterns in the codebase
- Break up complex functions (>20 lines) into smaller functions

## Testing Requirements

Every new feature or bugfix MUST be covered by unit tests:
- Unit tests: `tests/unit_tests/` (no network calls allowed)
- Integration tests: `tests/integration_tests/` (network calls permitted)

## Security

- No `eval()`, `exec()`, or `pickle` on user-controlled input
- Proper exception handling (no bare `except:`)
- Remove unreachable/commented code before committing

## Documentation Standards

Use Google-style docstrings with Args section for all public functions.

## Model References

Always use the latest generally available (GA) models when referencing LLMs in docstrings. Avoid preview or beta identifiers unless the model has no GA equivalent.

---

Source: https://github.com/langchain-ai/langchain
