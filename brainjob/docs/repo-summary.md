# jobbrainmine / Brainjob — Repo Summary

Source: https://github.com/brickwalllegend2000/jobbrainmine

## What does this project do?

**jobbrainmine** is a small repo that hosts **Brainjob** — a local, JSON-only job search tracker. There is no database, no YAML config, and no frontend build step.

Brainjob separates two concerns:

| Concern | Where it lives | Who edits it |
|---------|----------------|--------------|
| Employer posting (immutable) | `job.json` → `description_original.content` | Captured once; verified by SHA-256 |
| Your workflow | `application.json`, `contacts.json`, `notes.json`, `documents.json` | You, by hand |

A Python CLI manages the workspace:

- **`add`** — create a new job from templates
- **`validate`** — check JSON shape, cross-file consistency, and description integrity
- **`sync`** — regenerate `tracking/index.json` and `tracking/dashboard.html`
- **`sync --check`** — CI-friendly stale check
- **`watch`** — poll `data/jobs/` and auto-sync
- **`archive`** — move finished jobs to `data/jobs/_archive/`

The dashboard is a static HTML file (CSS/JS embedded at sync time) showing pipeline stats, filters, deadlines, the full original posting, timeline, contacts, notes, documents, and an integrity indicator.

**In one line:** Brainjob is a file-based personal CRM for job applications where the original vacancy text is never modified by tooling.

---

## Work breakdown

### 1. Data layer (authoritative)

| ID | Work package | Deliverables | Status |
|----|--------------|--------------|--------|
| 1.1 | Job record schema | `job.json` — role, location, compensation, dates, source, classification | Done |
| 1.2 | Application tracking | `application.json` — status, timeline, interviews, assessments, offer | Done |
| 1.3 | Contacts | `contacts.json` | Done |
| 1.4 | Personal notes | `notes.json` — `user` / `ai` authors, categories | Done |
| 1.5 | Document metadata | `documents.json` — CV/cover letter paths and submission state | Done |
| 1.6 | Templates | `data/templates/job/*.json` for `brainjob add` | Done |
| 1.7 | Example bundle | `data/jobs/example-company-policy-officer/` | Done |

### 2. Integrity and validation

| ID | Work package | Module | Status |
|----|--------------|--------|--------|
| 2.1 | SHA-256 stamping and verification | `integrity.py` | Done |
| 2.2 | Per-file schema validation | `schemas.py` | Done |
| 2.3 | Workspace validation report | `validate.py` | Done |
| 2.4 | Sync gate (no sync on validation failure) | `sync.py` | Done |

### 3. CLI (`brainjob`)

| ID | Command | Module | Status |
|----|---------|--------|--------|
| 3.1 | `add` | `add.py` | Done |
| 3.2 | `validate` | `validate.py` + `cli.py` | Done |
| 3.3 | `sync` / `sync --check` | `sync.py` | Done |
| 3.4 | `watch` | `watch.py` | Done |
| 3.5 | `archive <job-id>` | `archive.py` | Done |
| 3.6 | Root discovery (`--root`, `BRAINJOB_ROOT`) | `paths.py` | Done |

### 4. Generated tracking layer

| ID | Work package | Output | Status |
|----|--------------|--------|--------|
| 4.1 | Index aggregation | `tracking/index.json` — stats, jobs, integrity flags | Done |
| 4.2 | Dashboard rendering | `tracking/dashboard.html` | Done |
| 4.3 | Dashboard UI | `dashboard.css`, `dashboard.js` — filters, detail view | Done |
| 4.4 | Static assets slot | `tracking/assets/` | Placeholder only |

### 5. Quality and packaging

| ID | Work package | Status |
|----|--------------|--------|
| 5.1 | Unit/integration tests (12 tests) | Done |
| 5.2 | `pyproject.toml` + `brainjob` console script | Done |
| 5.3 | Documentation (`brainjob/README.md`) | Done |

### 6. Logical dependency flow

```
data/jobs/*.json  -->  validate  -->  sync  -->  index.json
                                              -->  dashboard.html
add / manual edit -->  data/jobs/*.json
watch             -->  sync
archive           -->  data/jobs/_archive/
```

---

## Suggested follow-on work (not in repo yet)

| Priority | Work package | Scope |
|----------|--------------|-------|
| P1 | Edit helpers | CLI for timeline events, note append, status transitions (without touching `description_original`) |
| P1 | CI workflow | GitHub Action running `validate` + `sync --check` |
| P2 | Import/scrape | `capture_method: scrape` pipeline that stamps hash at import |
| P2 | Document file linking | Resolve `documents.json` paths relative to job dir |
| P3 | Restore from archive | `brainjob restore <job-id>` |
| P3 | Search/export | Filter jobs to Markdown or CSV from `index.json` |

---

**Repo shape today:** one product (`brainjob/`), one example job, one generated dashboard, stdlib-only Python CLI, 12 tests.
