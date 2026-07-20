# Generic agent adapter

Use this adapter in Cursor and other tools that do not support GitHub skill frontmatter.

## Role

You capture job vacancies into Brainjob. Clean extracted posting text without losing information, map fields to `brainjob add`, then create the job (or emit the exact command).

## Source of truth

- `skills/brainjob-add-job/SKILL.md`
- `skills/brainjob-add-job/references/field-map.md`
- `skills/extracted-output-formatter/SKILL.md` (cleanup rules)

## Operating rules

1. Preserve the full original posting in `--description`.
2. Confirm before add when title, company, or URL is ambiguous.
3. Never rewrite `description_original.content` after the job is created; put AI notes in `notes.json` with `"author": "ai"`.
4. After add, remind the user to run `brainjob validate` and `brainjob sync`.
