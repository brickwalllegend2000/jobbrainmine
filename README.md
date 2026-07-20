# jobbrainmine

This repository contains [Brainjob](brainjob/README.md), a JSON-only job-search information system.

```bash
cd brainjob
python -m pip install -e ".[dev]"
brainjob validate
brainjob sync
```

## Dashboard

| Access | Link |
|--------|------|
| Live | [https://brickwalllegend2000.github.io/jobbrainmine/](https://brickwalllegend2000.github.io/jobbrainmine/) |
| Local | `http://localhost:8000/dashboard.html` (after the commands below) |

Serve the dashboard locally after syncing:

```bash
cd brainjob
brainjob sync
python -m http.server 8000 --directory tracking
```

Then open `http://localhost:8000/dashboard.html` on the same machine.

## CI and live dashboard

On pushes to `main` that change job data or sync code (or via **Actions → Sync tracking and publish Pages → Run workflow**), GitHub Actions:

1. Runs `brainjob validate` and `brainjob sync`
2. Commits updated `brainjob/tracking/` artifacts back to the repo
3. Publishes `tracking/dashboard.html` as the site root (`index.html`) to GitHub Pages

Live dashboard: [https://brickwalllegend2000.github.io/jobbrainmine/](https://brickwalllegend2000.github.io/jobbrainmine/)

Pull requests run pytest, validation, and `brainjob sync --check`.

## Docs

| Document | Description |
|----------|-------------|
| [Project summary](docs/project-summary.md) | Architecture and capabilities |
| [Work breakdown](docs/work-breakdown.md) | WBS and Plane backlog status |
| [JSON schema reference](docs/json-schema-reference.md) | Data model and formal schemas |
| [CHANGELOG](brainjob/CHANGELOG.md) | Version history |

## Skills

Cross-tool skill content lives under:

- `skills/`

GitHub-specific adapters live under:

- `.github/skills/`
