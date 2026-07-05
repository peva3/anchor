# Anchor — Rule Source of Truth

This directory is the single source of truth for agent instructions.
[Ruler](https://github.com/intellectronica/ruler) distributes these rules
to 30+ AI coding agents in their native formats.

## Usage

```bash
# Install Ruler
pip install ruler-agent

# Sync rules to all supported agents
ruler sync

# Sync with nested project rules
ruler sync --nested

# Revert to previous state
ruler revert
```

## Rule Files

Each `.md` file in `rules/` maps to one AGENTS.md section.
Ruler distributes them to the correct agent config locations.
