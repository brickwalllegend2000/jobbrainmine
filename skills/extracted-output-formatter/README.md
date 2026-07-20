# extracted-output-formatter (cross-tool canonical source)

This directory is the single source of truth for the skill content.

## Structure

- `SKILL.md` — canonical instructions and examples
- `references/format-specs.md` — shared format reference
- `adapters/` — tool-specific wrappers/metadata

## Adapters

- `adapters/github-copilot/SKILL.md` — GitHub Copilot adapter
- `adapters/generic-agent/PROMPT.md` — generic LLM/agent adapter template

## Sync rule

When updating the skill, edit canonical files first (`SKILL.md`, `references/*`) and then mirror only tool-specific wrapper/metadata in each adapter.
