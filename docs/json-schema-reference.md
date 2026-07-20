# Brainjob JSON schema reference

Human-readable guide to the Brainjob `schema_version: 1` data model.

**Runtime enforcer:** `brainjob/src/brainjob/schemas.py` (used by `brainjob validate`).
**Formal contracts:** `brainjob/schemas/*.schema.json` (JSON Schema Draft 2020-12 for editors and external tools).

Python validation remains the source of truth for CI. The `.schema.json` files document the same shape; they do not replace `schemas.py`. Cross-file `job_id` consistency and SHA-256 content immutability are Python-only checks.

## Per-job layout

Each active job lives at `brainjob/data/jobs/<job-id>/` with five JSON files:

| File | Schema | Purpose |
|------|--------|---------|
| `job.json` | [job.schema.json](../brainjob/schemas/job.schema.json) | Vacancy facts and immutable original posting |
| `application.json` | [application.schema.json](../brainjob/schemas/application.schema.json) | Pipeline status, timeline, interviews, assessments |
| `contacts.json` | [contacts.schema.json](../brainjob/schemas/contacts.schema.json) | People linked to the vacancy |
| `notes.json` | [notes.schema.json](../brainjob/schemas/notes.schema.json) | Personal or AI notes |
| `documents.json` | [documents.schema.json](../brainjob/schemas/documents.schema.json) | CV / cover letter metadata |

Archived jobs move to `data/jobs/_archive/<job-id>/` and are excluded from the dashboard index.

## Enums (must match `schemas.py`)

| Field | Allowed values |
|-------|----------------|
| `application.status` | `saved`, `preparing`, `applied`, `interviewing`, `assessment`, `offer`, `accepted`, `rejected`, `withdrawn`, `archived` |
| `notes[].author` | `user`, `ai` |
| `notes[].category` | `research`, `strategy`, `interview-prep`, `follow-up`, `general` |
| `documents[].type` | `cv`, `cover_letter`, `portfolio`, `other` |
| `job.source.posting_status` | `open`, `closed`, `unknown` |
| `job.classification.priority` | `low`, `medium`, `high` |
| `job.location.work_arrangement` | `on-site`, `hybrid`, `remote`, `unknown` |
| `job.source.capture_method` | `manual`, `import`, `scrape` |

## Immutability

1. `description_original.content` is employer-owned text. Tooling never rewrites it after capture.
2. `description_original.sha256` is a 64-character hex digest of that content.
3. Personal commentary belongs in `notes.json` (`author: user` or `author: ai`).
4. `tracking/index.json` and `tracking/dashboard.html` are generated; do not treat them as sources of truth.

## Required fields (summary)

### `job.json`

`schema_version` (const `1`), `id`, `role.title`, `role.company`, `location.display`, `compensation` (object), `dates.captured`, `source.url`, `description_original.content`, `description_original.sha256`, `classification` (object).

### `application.json`

`job_id`, `status`, `timeline` (array), `interviews` (array), `assessments` (array). If `next_action` is present, it must include `completed` (boolean).

### `contacts.json` / `notes.json` / `documents.json`

`job_id` plus the corresponding array (`contacts`, `notes`, or `documents`). Array item required fields: contact `name`; note `id`, `content`, `author`; document `type`, `path`, `submitted`.

## How to add a field

1. Update the matching file under `brainjob/schemas/`.
2. Update validation in `brainjob/src/brainjob/schemas.py`.
3. Update templates under `brainjob/data/templates/job/` and the example job if needed.
4. If the field is shown on the dashboard or index, update `sync.py` / dashboard assets and tests.
5. Update this document and `brainjob/CHANGELOG.md` `[Unreleased]`.
6. Keep `schema_version` at `1` unless the change is intentionally breaking (then plan a migration).
