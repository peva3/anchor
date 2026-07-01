# Anchor Audit Container
# Runs tests/test_agents_md_quality.py against the AGENTS.md template.
# Used by CI (.github/workflows/ci.yml) and locally for reproducible audits.

FROM python:3.12-slim

WORKDIR /repo

# Install only what the audit needs (pinned per Section 19).
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy the audit and the template it audits.
COPY tests/ tests/
COPY AGENTS.md .

# Default: run the audit. Override with `make audit` or pytest for unit tests.
ENTRYPOINT ["python3", "tests/test_agents_md_quality.py"]
