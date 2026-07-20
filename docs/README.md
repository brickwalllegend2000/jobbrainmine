# jobbrainmine documentation

Documentation for the [jobbrainmine](https://github.com/brickwalllegend2000/jobbrainmine) repository.

| Document | Description |
|----------|-------------|
| [Project summary](./project-summary.md) | What the project does, architecture, and current capabilities |
| [Work breakdown](./work-breakdown.md) | Work breakdown structure (WBS), including Plane backlog closure for JOBBRAINMI-1..9 and Phase A+B |
| [JSON schema reference](./json-schema-reference.md) | Human guide to schema_version 1 and formal `.schema.json` contracts |
| [Skill to job workflow](./skill-to-job-workflow.md) | Format extracted postings and create jobs with skills + `brainjob add` |
| [Phase A+B plan](./plans/2026-07-20-phase-a-b-hardening-and-tooling.md) | Implementation plan and Plane IDs JOBBRAINMI-10..16 |
| [CHANGELOG](../brainjob/CHANGELOG.md) | Brainjob version history |

## Dashboard

| Access | Link |
|--------|------|
| Live | [https://brickwalllegend2000.github.io/jobbrainmine/](https://brickwalllegend2000.github.io/jobbrainmine/) |
| Local | `http://localhost:8000/dashboard.html` |

## Quick start

```bash
cd brainjob
python -m pip install -e ".[dev]"
brainjob validate
brainjob sync
python -m http.server 8000 --directory tracking
```

Then open `http://localhost:8000/dashboard.html`, or use the [live dashboard](https://brickwalllegend2000.github.io/jobbrainmine/).
