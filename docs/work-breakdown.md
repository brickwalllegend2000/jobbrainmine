# Work breakdown: jobbrainmine

Work breakdown structure (WBS) for the **jobbrainmine** repository. Use this to plan development, onboarding, and maintenance.

Legend: **Done** = implemented in v0.1.0 | **Partial** = exists but limited | **Planned** = not yet built

---

## 1. Repository and documentation

| ID | Work package | Status | Notes |
|----|--------------|--------|-------|
| 1.1 | Root README with install pointer | Done | `README.md` |
| 1.2 | Brainjob README (commands, layout, immutability rules) | Done | `brainjob/README.md` |
| 1.3 | Docs folder (summary + WBS) | Done | `docs/` |
| 1.4 | CONTRIBUTING / development guide | Planned | Coding standards, PR flow |
| 1.5 | JSON schema reference (formal spec document) | Planned | Today validated in Python only |
| 1.6 | CHANGELOG | Planned | Version history |

---

## 2. Data layer

| ID | Work package | Status | Notes |
|----|--------------|--------|-------|
| 2.1 | Job directory layout (`data/jobs/<id>/`) | Done | Five required JSON files per job |
| 2.2 | Job templates for `brainjob add` | Done | `data/templates/job/` |
| 2.3 | Example job bundle | Done | `example-company-policy-officer` |
| 2.4 | Archive storage (`data/jobs/_archive/`) | Done | Excluded from active index |
| 2.5 | Schema versioning (`schema_version: 1`) | Done | In `job.json` and index |
| 2.6 | Import from external sources (scrape/API) | Planned | `capture_method: scrape` exists in schema but no importer |
| 2.7 | Bulk export (CSV, PDF report) | Planned | |
| 2.8 | Attachment/binary storage convention | Planned | Documents reference paths only today |

---

## 3. Core Python modules (`src/brainjob/`)

| ID | Work package | Module | Status | Responsibility |
|----|--------------|--------|--------|----------------|
| 3.1 | Path resolution and workspace discovery | `paths.py` | Done | Root detection, slugify, iter active jobs |
| 3.2 | JSON I/O helpers | `io.py` | Done | Load/save with consistent formatting |
| 3.3 | SHA-256 integrity | `integrity.py` | Done | Stamp and verify `description_original` |
| 3.4 | Schema validation | `schemas.py` | Done | Per-file and per-directory validation |
| 3.5 | Workspace validation report | `validate.py` | Done | Aggregate errors across jobs |
| 3.6 | Job creation from templates | `add.py` | Done | CLI-driven scaffolding |
| 3.7 | Index and dashboard generation | `sync.py` | Done | Stats, filters data, HTML render |
| 3.8 | File watcher | `watch.py` | Done | mtime polling, auto-sync |
| 3.9 | Archive workflow | `archive.py` | Done | Status update + directory move |
| 3.10 | CLI entry point | `cli.py` | Done | Subcommands, exit codes |
| 3.11 | Package metadata | `__init__.py`, `__main__.py` | Done | Version, `python -m brainjob` |

---

## 4. CLI surface

| ID | Command | Status | Key behaviors |
|----|---------|--------|---------------|
| 4.1 | `brainjob add` | Done | Required: title, company, description, url; optional location, deadline, tags |
| 4.2 | `brainjob validate` | Done | Non-zero exit on failure |
| 4.3 | `brainjob sync` | Done | Refuses when validation fails |
| 4.4 | `brainjob sync --check` | Done | CI-friendly staleness check |
| 4.5 | `brainjob watch` | Done | Configurable interval |
| 4.6 | `brainjob archive <job-id>` | Done | Idempotent guard if already archived |
| 4.7 | `brainjob edit` / interactive TUI | Planned | Today all edits are manual JSON |
| 4.8 | `brainjob status` (quick summary) | Planned | |
| 4.9 | `brainjob restore` (un-archive) | Planned | |

Global flags: `--root`, `BRAINJOB_ROOT`, `--version`.

---

## 5. Tracking and dashboard

| ID | Work package | Status | Notes |
|----|--------------|--------|-------|
| 5.1 | `tracking/index.json` generation | Done | Stats, per-job summary, integrity flags |
| 5.2 | Self-contained `dashboard.html` | Done | CSS/JS inlined at sync |
| 5.3 | Pipeline stats panel | Done | Counts by status, overdue, deadlines |
| 5.4 | Filters (status, priority, overdue, integrity, search) | Done | Client-side in `dashboard.js` |
| 5.5 | Job detail view (timeline, notes, documents) | Done | |
| 5.6 | `tracking/assets/` placeholder | Done | `.gitkeep` only |
| 5.7 | Live reload / dev server for dashboard | Planned | Today: re-sync and refresh browser |
| 5.8 | Dark mode / accessibility audit | Planned | |
| 5.9 | Export selected jobs from dashboard | Planned | |

---

## 6. Validation and data integrity

| ID | Work package | Status | Notes |
|----|--------------|--------|-------|
| 6.1 | Required field validation per file type | Done | `schemas.py` |
| 6.2 | Cross-file `job_id` consistency | Done | |
| 6.3 | SHA-256 verification of original description | Done | Tamper detection |
| 6.4 | Enum validation (status, author, doc type, etc.) | Done | |
| 6.5 | JSON Schema (.json) files for external tools | Planned | |
| 6.6 | Pre-commit hook integration | Planned | validate + sync --check |
| 6.7 | Migration tooling for `schema_version` bumps | Planned | |

---

## 7. Testing and quality

| ID | Work package | Status | Test file |
|----|--------------|--------|-----------|
| 7.1 | Integrity unit tests | Done | `test_integrity.py` (4 tests) |
| 7.2 | Add job integration test | Done | `test_add.py` |
| 7.3 | Validation tests (happy + tampered) | Done | `test_validate.py` |
| 7.4 | Sync and staleness check tests | Done | `test_sync.py` |
| 7.5 | Archive workflow test | Done | `test_archive.py` |
| 7.6 | CLI smoke tests | Done | `test_cli.py` |
| 7.7 | Dashboard JS tests | Planned | No frontend test runner yet |
| 7.8 | CI workflow (GitHub Actions) | Planned | pytest on push/PR |
| 7.9 | Coverage reporting | Planned | |
| 7.10 | Lint/typecheck (ruff, mypy) | Planned | |

**Current test count:** 13 tests across 6 files.

---

## 8. Packaging and distribution

| ID | Work package | Status | Notes |
|----|--------------|--------|-------|
| 8.1 | `pyproject.toml` with console script | Done | `brainjob` entry point |
| 8.2 | Editable install with dev extras | Done | `pip install -e ".[dev]"` |
| 8.3 | PyPI publish | Planned | |
| 8.4 | Docker image / devcontainer | Planned | |
| 8.5 | Homebrew / system package | Planned | |

---

## 9. Suggested development phases

Phases group the **Planned** items above into logical delivery order.

**Implementation plan (Phase A + B):** [plans/2026-07-20-phase-a-b-hardening-and-tooling.md](./plans/2026-07-20-phase-a-b-hardening-and-tooling.md) maps work to proposed Plane IDs **JOBBRAINMI-10..16**, file touches, acceptance criteria, and sequencing.

### Phase A -- Hardening (low risk, high value)

- 7.8 CI workflow (validate + pytest + sync --check) -- JOBBRAINMI-10
- 7.10 Lint (ruff) -- JOBBRAINMI-12
- 6.6 Pre-commit hooks -- JOBBRAINMI-11
- 1.6 CHANGELOG -- JOBBRAINMI-13

### Phase B -- Spec and tooling clarity

- 6.5 Formal JSON Schema files -- JOBBRAINMI-14
- 1.5 JSON schema reference document -- JOBBRAINMI-15
- 4.8 `brainjob status` quick summary command -- JOBBRAINMI-16

### Phase C -- Import and export

- 2.6 Job posting importer (URL or file)
- 2.7 Export to CSV/PDF
- 2.8 Document attachment conventions

### Phase D -- UX improvements

- 4.7 Interactive edit helper (status, next action, notes)
- 5.7 Dashboard dev workflow
- 5.8 Accessibility pass
- 4.9 Un-archive / restore

### Phase E -- Distribution

- 8.3 PyPI release
- 8.4 Docker/devcontainer

---

## 10. Dependency map (implementation order for new features)

When adding features, respect this dependency order:

```
paths.py / io.py
    └── integrity.py
        └── schemas.py
            └── validate.py
                ├── add.py
                ├── sync.py ── dashboard.css / dashboard.js
                ├── archive.py
                └── watch.py
                    └── cli.py
                        └── tests/*
```

Any change to JSON shape requires updates in: `schemas.py`, templates, example job, `sync.py` (if indexed fields change), dashboard JS (if displayed), and tests.

---

## 11. Ownership-friendly work slices

Small, independent tasks suitable for parallel work:

| Slice | Files touched | Effort |
|-------|---------------|--------|
| Add GitHub Actions CI | `.github/workflows/` | Small |
| JSON Schema export | `schemas/`, docs | Medium |
| `brainjob status` command | `cli.py`, new module, tests | Small |
| Pre-commit config | `.pre-commit-config.yaml` | Small |
| Dashboard dark mode | `dashboard.css`, `dashboard.js` | Small |
| Job URL scraper | new `import.py`, CLI, tests | Large |
| Restore from archive | `archive.py`, CLI, tests | Medium |

---

## 12. Plane backlog closure (JOBBRAINMI-1..9)

The Plane backlog items **JOBBRAINMI-1** through **JOBBRAINMI-9** describe the Brainjob v0.1.0 MVP. They are **Done** in this repository; no greenfield implementation remains for those issues.

| Plane ID | Issue name | Status | Primary implementation |
|----------|------------|--------|------------------------|
| JOBBRAINMI-7 | Repository scaffolding | Done | `brainjob/data/`, `src/brainjob/`, `tests/`, `tracking/` |
| JOBBRAINMI-4 | Canonical JSON schemas and file contracts | Done | `schemas.py`, templates under `data/templates/job/` |
| JOBBRAINMI-8 | Add and archive commands | Done | `add.py`, `archive.py`, CLI subcommands |
| JOBBRAINMI-5 | Validation and integrity checks | Done | `validate.py`, `integrity.py` |
| JOBBRAINMI-6 | Tracking index and dashboard | Done | `sync.py`, `dashboard.css`, `dashboard.js` |
| JOBBRAINMI-9 | Sync and sync-check workflows | Done | `sync_workspace` / `brainjob sync [--check]` (index + dashboard generation; `posting_status` / `last_verified` are schema fields, not live HTTP probes) |
| JOBBRAINMI-2 | Watch mode | Done | `watch.py` |
| JOBBRAINMI-3 | README and contributor guidance | Done | `brainjob/README.md`, `docs/` |
| JOBBRAINMI-1 | Comprehensive tests | Done | `brainjob/tests/` (pytest) |

**Out of scope for this closure:** live URL verification of employer postings, formal JSON Schema (`.json`) files, CI/pre-commit/CHANGELOG/ruff (WBS Phase A), and other Planned WBS items in sections 1–8 above.

---

## 13. Plane backlog -- Phase A + B (proposed)

Next Plane issues after MVP closure. Full implementation plan: [plans/2026-07-20-phase-a-b-hardening-and-tooling.md](./plans/2026-07-20-phase-a-b-hardening-and-tooling.md).

| Plane ID | Phase | WBS | Issue name | Status |
|----------|-------|-----|------------|--------|
| JOBBRAINMI-10 | A | 7.8 | CI workflow (pytest + validate + sync --check) | Planned |
| JOBBRAINMI-11 | A | 6.6 | Pre-commit hooks | Planned |
| JOBBRAINMI-12 | A | 7.10 | Ruff lint configuration | Planned |
| JOBBRAINMI-13 | A | 1.6 | CHANGELOG for v0.1.0 | Planned |
| JOBBRAINMI-14 | B | 6.5 | Formal JSON Schema files | Planned |
| JOBBRAINMI-15 | B | 1.5 | JSON schema reference document | Planned |
| JOBBRAINMI-16 | B | 4.8 | `brainjob status` command | Planned |

**Delivery order:** 10 → 12 → 11 → 13 → 14 → 15 → 16 (13 and 16 can parallelize once CI exists).
