# Changelog

All notable changes to Brainjob are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Dev tooling: ruff lint (`E`/`F`/`I`), pre-commit hooks (ruff, validate, sync --check)
- Formal JSON Schema contracts under `schemas/` (Draft 2020-12)
- JSON schema reference document at `docs/json-schema-reference.md`
- `brainjob status` pipeline summary command
- Live dashboard on GitHub Pages: https://brickwalllegend2000.github.io/jobbrainmine/

### Fixed

- Pages publish workflow CLI flag order (`brainjob --root …`) so deploys succeed

## [0.1.0] - 2026-07-20

### Added

- JSON-only per-job storage under `data/jobs/<job-id>/` with five files:
  `job.json`, `application.json`, `contacts.json`, `notes.json`, `documents.json`
- Immutable `description_original.content` with SHA-256 integrity verification
- CLI commands: `add`, `validate`, `sync`, `sync --check`, `watch`, `archive`
- Generated `tracking/index.json` and self-contained `tracking/dashboard.html`
- Job templates for `brainjob add` and example job bundle
- Archive workflow moving jobs to `data/jobs/_archive/`
- pytest suite covering integrity, add, validate, sync, archive, and CLI smoke
- GitHub Actions CI (pytest, validate, sync --check) and Pages sync publish
