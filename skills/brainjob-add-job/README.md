# brainjob-add-job (cross-tool canonical source)

This directory is the single source of truth for the skill content.

## Structure

- `SKILL.md` -- canonical instructions and workflow
- `references/field-map.md` -- extracted fields to `brainjob add` flags
- `adapters/` -- tool-specific wrappers/metadata

## Adapters

- `adapters/github-copilot/SKILL.md` -- GitHub Copilot adapter
- `adapters/generic-agent/PROMPT.md` -- Cursor and any non-frontmatter tool
- `adapters/claude/PROMPT.md` -- Claude Projects / custom instructions
- `adapters/chatgpt/PROMPT.md` -- ChatGPT Custom GPT / Project instructions

## Sync rule

When updating the skill, edit canonical files first (`SKILL.md`, `references/*`) and then mirror only tool-specific wrapper/metadata in each adapter.

Related human guide: [`docs/skill-to-job-workflow.md`](../../docs/skill-to-job-workflow.md).
