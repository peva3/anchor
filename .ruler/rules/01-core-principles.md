# 01-core-principles.md

- No dead code — every function must have a production call path
- No stubs — every component must have a real implementation
- No silent failures — log before swallowing exceptions
- Test-first — tests must pass before marking work complete
- Proven integration — verify end-to-end before declaring done
- Cross-service contract tests — exercise the real HTTP contracts between services
- Trace every function call — verify every public function is called by a production path

[Source: AGENTS.md Section 1]
