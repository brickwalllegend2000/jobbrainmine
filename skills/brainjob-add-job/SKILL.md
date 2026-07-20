---
name: brainjob-add-job
description: >
  Capture a job vacancy into Brainjob from messy posting text, OCR, scrapes, or
  LLM extracts. Use when the user asks to add a job, capture a posting, import a
  vacancy, or turn extracted job text into a brainjob record. Cleans the extract
  first (preserve full description), maps fields to brainjob add flags, then
  creates the job via the CLI (or emits a ready-to-run command).
---

# Brainjob Add Job

Turn a raw vacancy posting into a Brainjob job directory using `brainjob add`.

## When to use

- "Add this job", "capture this posting", "import this vacancy"
- User pastes a job ad, scrape, or OCR dump and wants it in `data/jobs/`
- Downstream of `extracted-output-formatter` when the target is Brainjob storage

## Core workflow

1. **Analyze the input** -- Identify title, company, source URL, location, deadline, tags, and the full original posting body.
2. **Clean without loss** -- Apply the same preserve-first rules as [`skills/extracted-output-formatter/SKILL.md`](../extracted-output-formatter/SKILL.md). Normalize dates to ISO `YYYY-MM-DD`. Do not summarize away the description.
3. **Confirm ambiguous fields** -- If title, company, or URL is unclear, ask before creating the job.
4. **Map fields** -- See [`references/field-map.md`](references/field-map.md).
5. **Create the job** -- From the `brainjob/` workspace root, run `brainjob add` with the mapped flags. If you cannot run a shell, emit the exact command for the user.
6. **Remind next steps** -- Optional JSON edits under `data/jobs/<job-id>/`, then `brainjob validate` and `brainjob sync`.

## Required vs optional

Required: `--title`, `--company`, `--description`, `--url`.

Optional: `--job-id`, `--department`, `--location`, `--city`, `--country`, `--deadline`, `--tags`, `--priority`.

## Immutability rules

1. Pass the **full original posting** as `--description`. After add, tooling stamps SHA-256 and must never rewrite `description_original.content`.
2. Put AI commentary or summaries in `notes.json` with `"author": "ai"`, not in `job.json` employer fields.
3. Treat `tracking/` as generated; authoritative data lives under `data/jobs/`.

## Example

User pastes a messy posting. After cleaning and confirmation:

```bash
cd brainjob
brainjob add \
  --title "Policy Officer" \
  --company "Example Company" \
  --description "Paste the full original posting here." \
  --url "https://example.com/jobs/policy-officer" \
  --location "Brussels, Belgium" \
  --city Brussels \
  --country Belgium \
  --deadline 2026-08-15 \
  --tags policy eu-affairs
```

Then:

```bash
brainjob validate
brainjob sync
```

## Best practices

- Prefer running `brainjob add` over hand-writing the five JSON files.
- Quote shell arguments that contain spaces or special characters.
- Flag duplicates (same company + title already present) and suggest `--job-id` only when needed.
- Keep cleanup separate from editorial rewrite: structure the posting; do not invent requirements that were not in the source.
