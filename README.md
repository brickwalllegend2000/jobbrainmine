# jobbrainmine

This repository contains [Brainjob](brainjob/README.md), a JSON-only job-search information system.

```bash
cd brainjob
python -m pip install -e ".[dev]"
brainjob validate
brainjob sync
```

Open `brainjob/tracking/dashboard.html` after syncing.

## CI and live dashboard

On pushes to `main` that change job data or sync code, GitHub Actions:

1. Runs `brainjob validate` and `brainjob sync`
2. Commits updated `brainjob/tracking/` artifacts back to the repo
3. Publishes the dashboard to GitHub Pages

After enabling Pages (Settings → Pages → Source: GitHub Actions), view it at:

`https://brickwalllegend2000.github.io/jobbrainmine/`

Pull requests run pytest, validation, and `brainjob sync --check`.
