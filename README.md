# jobbrainmine

This repository contains [Brainjob](brainjob/README.md), a JSON-only job-search information system.

```bash
cd brainjob
python -m pip install -e ".[dev]"
brainjob validate
brainjob sync
```

## Dashboard

| Access | Address | Requirement |
|--------|---------|-------------|
| Live | [Open the GitHub Pages dashboard](https://brickwalllegend2000.github.io/jobbrainmine/) | Latest Pages deployment must be successful |
| Local | `http://localhost:8000/dashboard.html` | Run the local server below on this computer |

Serve the dashboard locally after syncing:

```bash
cd brainjob
brainjob sync
python -m http.server 8000 --directory tracking
```

While that command is running, open `http://localhost:8000/dashboard.html` on the same computer.

## CI and live dashboard

On pushes to `main` that change job data or sync code, GitHub Actions:

1. Runs `brainjob validate` and `brainjob sync`
2. Commits updated `brainjob/tracking/` artifacts back to the repo
3. Publishes the dashboard to GitHub Pages

After enabling Pages (Settings → Pages → Source: GitHub Actions), view it at:

[https://brickwalllegend2000.github.io/jobbrainmine/](https://brickwalllegend2000.github.io/jobbrainmine/)

Pull requests run pytest, validation, and `brainjob sync --check`.

## Skills

Cross-tool skill content lives under:

- `skills/`

GitHub-specific adapters live under:

- `.github/skills/`
