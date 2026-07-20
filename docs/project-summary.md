# Project summary: jobbrainmine

## What does this project do?

**jobbrainmine** is a GitHub repository that hosts **Brainjob**, a local-first job-search information system. It helps you track job applications using plain JSON files on disk -- no database, no YAML config, and no frontend build step.

### Problem it solves

Job seekers often scatter vacancy details, application status, contacts, notes, and document metadata across spreadsheets, notes apps, and browser tabs. Brainjob centralizes that information in a predictable folder structure you can edit by hand, version in Git, and back up like any other files.

### Core design principles

1. **JSON-only storage** -- Each job is a directory of five JSON files under `brainjob/data/jobs/<job-id>/`.
2. **Immutable employer content** -- The original job posting text in `job.json` is treated as read-only. Tooling verifies it with SHA-256 and never rewrites it.
3. **Separation of concerns** -- Vacancy facts, application workflow, contacts, notes, and documents live in separate files.
4. **Generated views** -- `brainjob sync` builds `tracking/index.json` and a self-contained `tracking/dashboard.html` for browsing; these are derived artifacts, not sources of truth.

### Repository layout

```
jobbrainmine/
├── README.md                 # Top-level pointer to Brainjob
├── docs/                     # Project documentation (this folder)
└── brainjob/                 # The Brainjob application
    ├── data/
    │   ├── jobs/<job-id>/    # Authoritative job records (human-editable)
    │   └── templates/job/    # Templates for `brainjob add`
    ├── tracking/             # Generated index + dashboard
    ├── src/brainjob/         # Python CLI and dashboard assets
    └── tests/                # pytest suite
```

### Per-job data model

Each active job directory contains:

| File | Role |
|------|------|
| `job.json` | Vacancy record: role, location, compensation, dates, source URL, tags, and `description_original` (immutable posting text + SHA-256) |
| `application.json` | Pipeline status, timeline, interviews, assessments, offer, next actions |
| `contacts.json` | People associated with the vacancy |
| `notes.json` | Personal or AI-authored notes (`author`: `user` or `ai`) |
| `documents.json` | CV, cover letter, and other document metadata with submission state |

Archived jobs move to `data/jobs/_archive/<job-id>/` and are excluded from the dashboard index.

### CLI commands

| Command | Purpose |
|---------|---------|
| `brainjob add` | Create a new job from templates; stamps `description_original.sha256` at capture time |
| `brainjob validate` | Check JSON shape, cross-file `job_id` consistency, and description integrity |
| `brainjob sync` | Regenerate `tracking/index.json` and `tracking/dashboard.html` (aborts if validation fails) |
| `brainjob sync --check` | Exit 0 when tracking artifacts are up to date; exit 1 when stale or missing |
| `brainjob watch` | Poll `data/jobs/` and auto-sync on JSON changes |
| `brainjob archive <job-id>` | Mark archived, append timeline event, move directory to `_archive/` |
| `brainjob status` | Print pipeline summary (counts, overdue actions, deadlines) without writing tracking |

### Dashboard

| Access | Link |
|--------|------|
| Live | [https://brickwalllegend2000.github.io/jobbrainmine/](https://brickwalllegend2000.github.io/jobbrainmine/) |
| Local | `http://localhost:8000/dashboard.html` after `brainjob sync` and `python -m http.server 8000 --directory tracking` |

The dashboard embeds job data at sync time and provides:

- Pipeline stats and status/priority filters
- Overdue next actions and upcoming deadlines
- Full original job description view
- Application timeline, interviews, and assessments
- Contacts, notes, and document submission tracking
- SHA-256 integrity indicator for original posting content

### Technology stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.10+ |
| Dependencies | Zero runtime dependencies (stdlib only) |
| Dev dependencies | pytest, ruff, pre-commit |
| Packaging | setuptools (`pyproject.toml`) |
| Frontend | Vanilla HTML/CSS/JS inlined at sync time |
| License | MIT |

### Agent skills

Cross-tool skills under [`skills/`](../skills/) help capture vacancies from messy posting text:

| Skill | Role |
|-------|------|
| `extracted-output-formatter` | Clean OCR/scrape/LLM extracts without losing information |
| `brainjob-add-job` | Map fields and create a job via `brainjob add` |

Adapters cover GitHub Copilot, Cursor/generic agents, Claude, and ChatGPT. End-to-end guide: [skill-to-job-workflow.md](./skill-to-job-workflow.md).

### Current maturity

- **Version:** 0.1.0 ([CHANGELOG](../brainjob/CHANGELOG.md)); Unreleased notes cover Pages, skills workflow, and `add` multiline fix
- **Status:** Functional MVP with CLI, validation, sync, watch, archive, status, dashboard, formal JSON schemas, sample jobs, agent skills, and test coverage across all major modules
- **History:** Initial commit plus feature PRs for the JSON-only system, CI/Pages, docs, Phase A+B hardening, and skill-to-job capture workflow
- **Plane backlog:** JOBBRAINMI-1 through JOBBRAINMI-9 (MVP) and JOBBRAINMI-10 through JOBBRAINMI-16 (Phase A+B) are Done (see [work-breakdown.md](./work-breakdown.md) sections 12–13)

### Example workflow

```bash
cd brainjob
python -m pip install -e ".[dev]"

# Add a vacancy from a posting (multiline --description is supported)
brainjob add \
  --title "Policy Officer" \
  --company "Example Company" \
  --description "Paste the full original posting here." \
  --url "https://example.com/jobs/policy-officer" \
  --location "Brussels, Belgium" \
  --deadline 2026-08-15 \
  --tags policy eu-affairs

# Edit JSON files under data/jobs/<job-id>/ by hand (status, notes, contacts, etc.)

brainjob validate
brainjob sync

# Local: python -m http.server 8000 --directory tracking
# Live:  https://brickwalllegend2000.github.io/jobbrainmine/
```

For agent-assisted capture (format then add), see [skill-to-job-workflow.md](./skill-to-job-workflow.md).

Sample job bundles under `brainjob/data/jobs/`:

| Job id | Role |
|--------|------|
| `example-company-policy-officer` | Spec sample (synthetic) |
| `green-european-foundation-policy-consultant-on-green-transition` | Real capture from call PDF text |
