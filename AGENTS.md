# AGENTS.md

Guidance for agents working in this repo (**jobbrainmine**). Deep detail lives in `brainjob/README.md`, `docs/`, and `docs/json-schema-reference.md`; this file captures the high-level map plus non-obvious conventions. Prefer referencing those docs over duplicating them.

## Project overview

Brainjob is a JSON-only job-search information system. Authoritative, human-editable job records live under `brainjob/data/jobs/<job-id>/`; employer content in `job.json` is treated as immutable. There is no database, no build step, and no runtime dependencies (dev deps: `pytest`, `ruff`, `pre-commit`). The only "service" is a static dashboard.

Layout:

- `brainjob/src/brainjob/` -- the Python CLI package (entry point `brainjob = brainjob.cli:main`).
- `brainjob/data/jobs/<id>/` -- authoritative per-job records; `brainjob/data/templates/job/` -- templates for `brainjob add`.
- `brainjob/schemas/` -- formal JSON Schema (Draft 2020-12) contracts for editors/docs only.
- `brainjob/tracking/` -- generated `index.json` + `dashboard.html` (never hand-edit).
- `brainjob/tests/` -- pytest suite. `docs/`, `skills/`, `.github/` -- docs, cross-tool skills, CI + Copilot skill stubs.

## Architecture and data flow

- CLI is argparse-based (`cli.py`) with subcommands `add`, `validate`, `sync`, `watch`, `archive`, `status`. Global `--root` and env `BRAINJOB_ROOT` set the workspace; otherwise the root is auto-detected by walking up until a dir contains both `data/jobs/` and `tracking/` (`paths.find_root`).
- Each active job dir has exactly five files: `job.json`, `application.json`, `contacts.json`, `notes.json`, `documents.json`. Every satellite file's `job_id` and `job.json`'s `id` must equal the directory name.
- Flow: `add` renders templates and stamps `description_original.sha256` -> `validate` checks shape + cross-file ids + SHA-256 integrity -> `sync` (validation-gated) denormalizes all jobs into `tracking/index.json` and inlines `dashboard.css`/`dashboard.js` + the index JSON into `tracking/dashboard.html`.
- Runtime validation is **custom hand-written Python in `schemas.py`** (not the `jsonschema` library); the `schemas/*.schema.json` files are documentation/editor contracts and allow `additionalProperties`. Changing an enum means updating both the frozenset in `schemas.py` and the matching `.schema.json`.
- Active jobs exclude dirs starting with `_` or `.`; `archive` moves a job to `data/jobs/_archive/<id>/`, so it drops out of the index on next sync.

## Key conventions and gotchas

- `add` does NOT sync; new jobs are invisible in tracking/dashboard until `brainjob sync` (or `brainjob watch`).
- `sync` refuses to run if validation fails, so any integrity/schema error blocks the whole dashboard regeneration.
- Editing `description_original.content` without updating `sha256` fails validation; there is no re-stamp helper (only `add` stamps). Personal/AI commentary belongs in `notes.json` (`author: "ai"` for AI).
- `sync --check` ignores `generated_at` but compares everything else, including date-relative `overdue_action` flags -- so committed tracking can go stale purely with the passage of time (this is the recurring `CI / test` failure on `main`).
- `add.py` stamps timestamps in `Europe/Brussels`; `sync`/`status`/`archive` use the local/system timezone for overdue/deadline math.
- Date-sensitive tests inject `today=` (see `test_status.py`); the integrity test pins a known SHA-256 for a specific example string. Tests must use `tmp_path`/`isolated_workspace` and copy templates when exercising `add`; never mutate committed `tracking/` or job data.
- Two CI workflows: `.github/workflows/ci.yml` (lint/test/validate/sync-check on every PR and `main` push) and `sync-and-publish.yml` (path-filtered `main` pushes: regenerates tracking, commits with `[skip ci]`, and publishes the dashboard to GitHub Pages). Both use Python 3.12 even though `pyproject.toml` allows 3.10+.
- Cross-tool skills are canonical under `skills/<name>/`; `.github/skills/` and per-skill `adapters/` are thin wrappers -- edit the canonical `SKILL.md`/`references/` first.

## Cursor Cloud specific instructions

Brainjob is a single Python 3 CLI package (`brainjob/`) with no runtime dependencies. It has no long-running backend; the only "service" is a static dashboard served by `python -m http.server`. Standard install/lint/test/run commands are documented in `brainjob/README.md` and `.github/workflows/ci.yml`; prefer those.

Non-obvious notes:

- The `brainjob` console script installs to `~/.local/bin` (user install, no venv). That dir is added to `PATH` via `~/.bashrc`, so `brainjob`, `pytest`, and `ruff` are available in new shells. If a command is "not found", run `export PATH="$HOME/.local/bin:$PATH"`.
- Run CLI commands from the `brainjob/` directory (or pass `--root` / set `BRAINJOB_ROOT`); paths are resolved relative to that workspace root.
- CI (`.github/workflows/ci.yml`) runs from `brainjob/`: `ruff check src tests`, `python -m pytest`, `brainjob validate`, `brainjob sync --check`.
- `tracking/index.json` and `tracking/dashboard.html` are generated by `brainjob sync`. `brainjob sync --check` exits 1 when they are stale. On a fresh checkout these can be stale; running `brainjob sync` regenerates them. Do NOT hand-edit tracking files, and avoid committing regenerated tracking artifacts unless the underlying job data actually changed.
- Dashboard: `brainjob sync` then `python -m http.server 8000 --directory tracking`, open `http://localhost:8000/dashboard.html`. Data is embedded at sync time, so re-run `brainjob sync` after changing job JSON.
- `brainjob validate` verifies the SHA-256 of `description_original.content` in each `job.json`; that content is treated as immutable employer text.
