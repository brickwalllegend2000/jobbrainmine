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
| Live (GitHub Pages) | [https://brickwalllegend2000.github.io/jobbrainmine/](https://brickwalllegend2000.github.io/jobbrainmine/) (after a successful Pages deploy) |
| Local | [http://localhost:8000/dashboard.html](http://localhost:8000/dashboard.html) |

Serve the dashboard locally after syncing:

```bash
cd brainjob
brainjob sync
python -m http.server 8000 --directory tracking
```

Then open [http://localhost:8000/dashboard.html](http://localhost:8000/dashboard.html).

## CI and live dashboard

On pushes to `main` that change job data or sync code (or via **Actions → Sync tracking and publish Pages → Run workflow**):

1. Runs `brainjob validate` and `brainjob sync`
2. Commits updated `brainjob/tracking/` artifacts back to the repo
3. Publishes `tracking/dashboard.html` as the site root (`index.html`) to GitHub Pages

Pages source must be **GitHub Actions** (Settings → Pages). Live URL:

[https://brickwalllegend2000.github.io/jobbrainmine/](https://brickwalllegend2000.github.io/jobbrainmine/)

Pull requests run pytest, validation, and `brainjob sync --check`.

## Skills

Cross-tool skill content lives under:

- `skills/`

GitHub-specific adapters live under:

- `.github/skills/`
