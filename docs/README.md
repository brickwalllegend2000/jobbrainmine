# jobbrainmine documentation

Documentation for the [jobbrainmine](https://github.com/brickwalllegend2000/jobbrainmine) repository.

| Document | Description |
|----------|-------------|
| [Project summary](./project-summary.md) | What the project does, architecture, and current capabilities |
| [Work breakdown](./work-breakdown.md) | Work breakdown structure (WBS), including Plane backlog closure for JOBBRAINMI-1..9 |
| [JSON schema reference](./json-schema-reference.md) | Human guide to schema_version 1 and formal `.schema.json` contracts |
| [Phase A+B plan](./plans/2026-07-20-phase-a-b-hardening-and-tooling.md) | Implementation plan and proposed Plane IDs JOBBRAINMI-10..16 for hardening and tooling |

## Quick start

```bash
cd brainjob
python -m pip install -e ".[dev]"
brainjob validate
brainjob sync
```

Open `brainjob/tracking/dashboard.html` in a browser after syncing.
