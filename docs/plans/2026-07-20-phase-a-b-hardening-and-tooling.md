# Phase A + Phase B Implementation Plan

> **For agentic workers:** Implement task-by-task in Plane ID order. Prefer one PR per Plane ticket (or one PR per phase if bundling). Use checkbox steps for tracking.

**Goal:** Harden the Brainjob MVP (CI, hooks, lint, changelog) and add schema/tooling clarity (formal JSON Schema, schema docs, `brainjob status`) so v0.1.0 is safe to extend.

**Architecture:** Keep zero runtime dependencies. Add only **dev** tooling (pytest already present; add ruff + pre-commit). Formal JSON Schema files live under `brainjob/schemas/` as documentation/contract artifacts; Python `schemas.py` remains the runtime validator. `brainjob status` reads active jobs the same way `sync`/`validate` do and prints a concise summary without rewriting tracking artifacts.

**Tech stack:** Python 3.10+, stdlib runtime, pytest, ruff, pre-commit, GitHub Actions, Draft 2020-12 JSON Schema.

**Origin:** [docs/work-breakdown.md](../work-breakdown.md) Phase A (section 9) and Phase B; Plane MVP closure JOBBRAINMI-1..9 is Done.

## Global constraints

- Runtime deps stay empty (`pyproject.toml` `[project].dependencies = []`).
- Do not change `schema_version` (stays `1`) unless a real breaking shape change is required -- Phase B documents the existing shape; it does not redesign it.
- Do not rewrite `description_original.content` or its SHA-256.
- Tracking files (`tracking/index.json`, `tracking/dashboard.html`) remain generated; never hand-edit as source of truth.
- Match existing CLI style in `src/brainjob/cli.py` (argparse subcommands, exit 0/1).
- Tests live under `brainjob/tests/`; use `workspace_root` fixture from `conftest.py`.

## Plane backlog (proposed IDs)

| Plane ID | Phase | WBS | Title |
|----------|-------|-----|-------|
| JOBBRAINMI-10 | A | 7.8 | CI workflow (pytest + validate + sync --check) |
| JOBBRAINMI-11 | A | 6.6 | Pre-commit hooks |
| JOBBRAINMI-12 | A | 7.10 | Ruff lint configuration |
| JOBBRAINMI-13 | A | 1.6 | CHANGELOG for v0.1.0 |
| JOBBRAINMI-14 | B | 6.5 | Formal JSON Schema files |
| JOBBRAINMI-15 | B | 1.5 | JSON schema reference document |
| JOBBRAINMI-16 | B | 4.8 | `brainjob status` command |

**Suggested Plane project labels:** `phase-a`, `phase-b`, `brainjob`. Priority: 10 > 12 > 11 > 13 for Phase A; then 14 > 15 > 16 for Phase B (14 before 15 so the doc can link real files).

---

## File map

| Path | Role | Created by |
|------|------|------------|
| `.github/workflows/ci.yml` | Push/PR CI | JOBBRAINMI-10 |
| `.pre-commit-config.yaml` | Local hooks | JOBBRAINMI-11 |
| `brainjob/pyproject.toml` | Add `[tool.ruff]`, optional `dev` extras | JOBBRAINMI-12 |
| `brainjob/CHANGELOG.md` | Version history | JOBBRAINMI-13 |
| `brainjob/schemas/*.schema.json` | Formal contracts | JOBBRAINMI-14 |
| `docs/json-schema-reference.md` | Human schema guide | JOBBRAINMI-15 |
| `brainjob/src/brainjob/status.py` | Status summary logic | JOBBRAINMI-16 |
| `brainjob/src/brainjob/cli.py` | Wire `status` subcommand | JOBBRAINMI-16 |
| `brainjob/tests/test_status.py` | Status tests | JOBBRAINMI-16 |
| `docs/work-breakdown.md` | Mark items Done as tickets close | each ticket |
| `docs/README.md` | Link new docs | JOBBRAINMI-13 / 15 |

---

## Phase A -- Hardening

### Task 1: JOBBRAINMI-10 -- CI workflow

**Files:**
- Create: `.github/workflows/ci.yml`
- Modify: none required in Python package

**Approach:**
- Trigger on `push` and `pull_request` to `main`.
- Job matrix optional; start with single `ubuntu-latest` + Python 3.10 (matches `requires-python`).
- Steps: checkout -> setup-python -> `pip install -e ".[dev]"` from `brainjob/` -> `pytest` -> `brainjob validate` -> `brainjob sync --check`.
- Working directory: `brainjob` for install and CLI; repo root for checkout.
- `sync --check` needs existing tracking artifacts committed (they already are). If check fails because generated files drifted, fail the job (correct behavior).

**Acceptance:**
- [ ] Workflow file exists and is valid YAML.
- [ ] On a clean tree, CI would pass: pytest green, validate exit 0, sync --check exit 0.
- [ ] Workflow does not publish packages or require secrets.

**Verify locally:**

```bash
cd brainjob
python -m pip install -e ".[dev]"
pytest
brainjob validate
brainjob sync --check
```

**Commit message:** `ci: add GitHub Actions for pytest validate and sync-check`

---

### Task 2: JOBBRAINMI-12 -- Ruff lint (before pre-commit so hooks have a target)

**Files:**
- Modify: `brainjob/pyproject.toml` -- add ruff to `[project.optional-dependencies].dev` and `[tool.ruff]` / `[tool.ruff.lint]`
- Optionally create: no separate `ruff.toml` (keep config in pyproject)

**Approach:**
- Add `ruff>=0.6` to `dev` extras.
- Target Python 3.10; `src` layout (`src = ["src"]` or lint `src` + `tests`).
- Start with a conservative rule set: `E`, `F`, `I` (pycodestyle errors, pyflakes, isort). Avoid enabling noisy rules that force a large reformat in the same PR unless the tree is already clean.
- First PR: config + fix any violations found so `ruff check src tests` is green.
- Do **not** enable `ruff format` as a hard CI gate in the same ticket unless the diff stays small; formatting can follow in a follow-up if needed.

**Acceptance:**
- [ ] `pip install -e ".[dev]"` installs ruff.
- [ ] `ruff check src tests` exits 0 from `brainjob/`.
- [ ] CI (Task 1) gains a `ruff check` step once this lands (amend workflow in this ticket or a tiny follow-up commit on the same branch).

**Verify:**

```bash
cd brainjob
ruff check src tests
```

**Commit message:** `chore(brainjob): add ruff lint config and clean violations`

---

### Task 3: JOBBRAINMI-11 -- Pre-commit hooks

**Files:**
- Create: `.pre-commit-config.yaml` (repo root)
- Modify: `brainjob/README.md` or `docs/` -- one short "Development" note on installing hooks

**Approach:**
- Hooks:
  1. `ruff` / `ruff-check` (mirror CI)
  2. Local hook: `brainjob validate` with `language: system` or `language: python` after install -- prefer documenting `pip install -e ".[dev]"` then pre-commit; use a local repo hook:

```yaml
- repo: local
  hooks:
    - id: brainjob-validate
      name: brainjob validate
      entry: brainjob validate
      language: system
      pass_filenames: false
      files: ^brainjob/data/.*\.json$
    - id: brainjob-sync-check
      name: brainjob sync --check
      entry: brainjob sync --check
      language: system
      pass_filenames: false
      files: ^brainjob/(data|tracking)/
```

- Also include standard `pre-commit-hooks` basics if useful (`trailing-whitespace`, `end-of-file-fixer`) -- keep minimal.
- Do not require pre-commit in CI beyond what CI already runs; pre-commit is for local DX.
- Document: `pre-commit install` from repo root after `pip install pre-commit`.

**Acceptance:**
- [ ] `.pre-commit-config.yaml` present at repo root.
- [ ] README/docs mention install steps.
- [ ] Hooks are idempotent and do not rewrite job JSON content.

**Commit message:** `chore: add pre-commit hooks for ruff validate and sync-check`

---

### Task 4: JOBBRAINMI-13 -- CHANGELOG

**Files:**
- Create: `brainjob/CHANGELOG.md` (Keep a Changelog format)
- Modify: `docs/project-summary.md` -- link CHANGELOG under maturity
- Modify: `docs/README.md` -- optional link

**Approach:**
- Document `[0.1.0]` as the MVP release date (use 2026-07-20 or the date of the feature PR merge) with Added sections covering CLI commands, JSON layout, dashboard, integrity, tests.
- Add an `[Unreleased]` section at top for Phase A/B follow-ups.
- No version bump in this ticket (stay on 0.1.0 until a real release cut).

**Acceptance:**
- [ ] CHANGELOG exists and lists 0.1.0 capabilities accurately.
- [ ] Docs link to it.

**Commit message:** `docs(brainjob): add CHANGELOG for v0.1.0`

---

### Phase A exit criteria

- [ ] CI green on `main` / PRs
- [ ] Ruff clean
- [ ] Pre-commit documented and usable
- [ ] CHANGELOG present
- [ ] WBS items 7.8, 6.6, 7.10, 1.6 marked **Done** in `docs/work-breakdown.md`

---

## Phase B -- Spec and tooling clarity

### Task 5: JOBBRAINMI-14 -- Formal JSON Schema files

**Files:**
- Create: `brainjob/schemas/job.schema.json`
- Create: `brainjob/schemas/application.schema.json`
- Create: `brainjob/schemas/contacts.schema.json`
- Create: `brainjob/schemas/notes.schema.json`
- Create: `brainjob/schemas/documents.schema.json`
- Create (optional): `brainjob/schemas/index.schema.json` for `tracking/index.json`
- Modify: `brainjob/README.md` -- point to `schemas/`
- Do **not** replace `schemas.py` runtime validation in this ticket

**Approach:**
- Mirror enums and required fields from `src/brainjob/schemas.py` (`APPLICATION_STATUSES`, `NOTE_AUTHORS`, etc.).
- Use `$schema`: `https://json-schema.org/draft/2020-12/schema`.
- One schema file per job JSON file type; `$id` relative or path-based.
- Cross-file `job_id` consistency stays a Python-only rule (document that limitation in schema descriptions / reference doc).
- SHA-256 format: string pattern for hex length 64 on `description_original.sha256`; content immutability remains a process/Python check.
- Optional lightweight test: if adding a dependency is undesirable, skip automated JSON Schema validation in CI for now **or** add `jsonschema` as a **dev-only** extra and one test that example job files validate. Prefer documenting external validation (`check-jsonschema`) over adding runtime coupling.
- **Decision (locked):** Python remains source of truth for CI validation; `.schema.json` files are contracts for editors and external tools. A future ticket may add `jsonschema` to dev and assert parity.

**Acceptance:**
- [ ] Five job file schemas cover the example job under `data/jobs/example-company-policy-officer/`.
- [ ] Enums match `schemas.py`.
- [ ] README links to `schemas/`.

**Commit message:** `docs(brainjob): add formal JSON Schema contracts for job files`

---

### Task 6: JOBBRAINMI-15 -- JSON schema reference document

**Files:**
- Create: `docs/json-schema-reference.md`
- Modify: `docs/README.md` -- add table row
- Modify: `docs/work-breakdown.md` -- mark 1.5 Done when shipped

**Approach:**
- Document per-file purpose, required fields, enums, immutability rules, archive layout, and that `schema_version: 1` is current.
- Link to `brainjob/schemas/*.schema.json` and to `schemas.py` as runtime enforcer.
- Include a short "how to add a field" checklist: update schema JSON, `schemas.py`, templates, example job, sync/index if needed, tests, this doc.
- No new code.

**Acceptance:**
- [ ] Doc is accurate against templates + `schemas.py`.
- [ ] Linked from `docs/README.md`.

**Commit message:** `docs: add JSON schema reference for Brainjob data model`

---

### Task 7: JOBBRAINMI-16 -- `brainjob status` command

**Files:**
- Create: `brainjob/src/brainjob/status.py`
- Create: `brainjob/tests/test_status.py`
- Modify: `brainjob/src/brainjob/cli.py` -- add `status` subparser and dispatch
- Modify: `brainjob/README.md` -- document command
- Modify: `docs/work-breakdown.md` -- mark 4.8 Done

**Interfaces:**
- Produces: `status_workspace(root: Path) -> StatusReport` (dataclass) and `format_status(report: StatusReport) -> str`
- Consumes: `iter_active_job_dirs`, `load_json`, existing application status enums; optionally reuse overdue logic from `sync.py` (`_is_overdue`) -- **prefer extracting a tiny shared helper** only if needed; otherwise duplicate the small date check to avoid a risky sync refactor in the same ticket.
- CLI: `brainjob status` prints to stdout, exit 0 even when there are overdue items (overdue is information, not failure). Exit 1 only on missing root / unreadable workspace. Invalid JSON: either skip-with-warning or fail -- **locked decision:** run `validate_workspace` first; if not ok, print validation failure and exit 1 (same spirit as sync refusing bad data).

**Output shape (directional):**

```
Jobs: 1
By status: preparing=1
Overdue next actions: 0
Upcoming deadlines: 1
Next actions:
  - example-company-policy-officer: Prepare cover letter (due 2026-07-28)
```

Keep stable enough for humans; do not promise machine-stable output in v1 (no `--json` unless cheap -- **YAGNI:** text only in this ticket).

**Test scenarios (`tests/test_status.py`):**
1. Empty jobs dir -> totals 0, exit 0 via CLI.
2. Example/`workspace_root` fixture -> counts match application statuses present.
3. Job with overdue next_action -> overdue count >= 1.
4. Invalid job JSON -> CLI exit 1.

**Acceptance:**
- [ ] `brainjob status` listed in `--help`.
- [ ] Tests cover scenarios above.
- [ ] README documents the command.
- [ ] No tracking files written.

**Commit message:** `feat(brainjob): add status command for pipeline summary`

---

### Phase B exit criteria

- [ ] Formal schemas + reference doc published
- [ ] `brainjob status` shipped with tests
- [ ] WBS items 6.5, 1.5, 4.8 marked **Done**
- [ ] CHANGELOG `[Unreleased]` updated with Phase B notes (or bump prep)

---

## Sequencing and dependencies

```
JOBBRAINMI-10 (CI)
    └── JOBBRAINMI-12 (ruff) ── adds ruff step to CI
            └── JOBBRAINMI-11 (pre-commit) ── wraps ruff + validate + sync --check
JOBBRAINMI-13 (CHANGELOG) ── independent; can parallelize with 10

JOBBRAINMI-14 (JSON Schema files)
    └── JOBBRAINMI-15 (reference doc) ── links to files from 14
JOBBRAINMI-16 (status) ── independent of 14/15; can parallelize after Phase A CI exists
```

**Recommended delivery order:** 10 → 12 → 11 → 13 → 14 → 15 → 16.

**Parallelism:** 13 with 10; 16 with 14/15 after CI is green.

---

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Ruff floods the PR with style noise | Enable only E/F/I first; format later |
| JSON Schema drifts from `schemas.py` | Reference doc checklist; optional later parity test |
| `sync --check` flakes on timestamp-only drift | Confirm check compares meaningful content (existing behavior); do not "fix" by rewriting index in CI |
| Pre-commit `language: system` fails for contributors without install | Document `pip install -e ".[dev]"` + PATH; keep CI as source of truth |
| Status duplicates sync logic | Accept small duplication; extract shared helpers only if both change again |

---

## Out of scope (do not sneak in)

- Phase C import/export, Phase D edit/restore/dashboard polish, Phase E PyPI/Docker
- Live URL verification of employer postings
- Replacing Python validation with JSON Schema at runtime
- `brainjob status --json`
- Version bump to 0.2.0 (unless releasing after both phases)

---

## Implementation checklist (executor)

Phase A:
- [ ] JOBBRAINMI-10 CI
- [ ] JOBBRAINMI-12 ruff
- [ ] JOBBRAINMI-11 pre-commit
- [ ] JOBBRAINMI-13 CHANGELOG
- [ ] Update WBS statuses for Phase A items

Phase B:
- [ ] JOBBRAINMI-14 schema JSON files
- [ ] JOBBRAINMI-15 reference doc
- [ ] JOBBRAINMI-16 `brainjob status`
- [ ] Update WBS statuses for Phase B items
- [ ] Refresh CHANGELOG Unreleased

---

## Spec coverage self-check

| WBS / request | Task |
|---------------|------|
| 7.8 CI | Task 1 / JOBBRAINMI-10 |
| 6.6 Pre-commit | Task 3 / JOBBRAINMI-11 |
| 7.10 Lint ruff | Task 2 / JOBBRAINMI-12 |
| 1.6 CHANGELOG | Task 4 / JOBBRAINMI-13 |
| 6.5 Formal JSON Schema | Task 5 / JOBBRAINMI-14 |
| 1.5 Schema reference doc | Task 6 / JOBBRAINMI-15 |
| 4.8 `brainjob status` | Task 7 / JOBBRAINMI-16 |
| Plane ticket mapping | Proposed IDs table above |
| Implementation how-to | Approach + files + verify + acceptance per task |
