# jobbrainmine

This repository contains [Brainjob](brainjob/README.md), a JSON-only job-search information system.

```bash
cd brainjob
python -m pip install -e ".[dev]"
brainjob validate
brainjob sync
```

Open `brainjob/tracking/dashboard.html` after syncing.

## Skills

Cross-tool skill content lives under:

- `/home/runner/work/jobbrainmine/jobbrainmine/skills/`

GitHub-specific adapters live under:

- `/home/runner/work/jobbrainmine/jobbrainmine/.github/skills/`
