# jobbrainmine documentation

Documentation for the [jobbrainmine](https://github.com/brickwalllegend2000/jobbrainmine) repository.

| Document | Description |
|----------|-------------|
| [Project summary](./project-summary.md) | What the project does, architecture, and current capabilities |
| [Work breakdown](./work-breakdown.md) | Work breakdown structure (WBS), including Plane backlog, Phase A+B, and profile library (section 14) |
| [JSON schema reference](./json-schema-reference.md) | Human guide to schema_version 1 and formal `.schema.json` contracts |
| [Skill to job workflow](./skill-to-job-workflow.md) | Format extracted postings and create jobs with skills + `brainjob add` (includes GEF worked example) |
| [Phase A+B plan](./plans/2026-07-20-phase-a-b-hardening-and-tooling.md) | Implementation plan and Plane IDs JOBBRAINMI-10..16 |
| [Profile source library plan](./plans/2026-07-21-profile-source-library.md) | Plane blueprint + Phase 1/2 delivery breakdown for standalone `profile/` (scaffold Planned) |
| [CHANGELOG](../brainjob/CHANGELOG.md) | Brainjob version history |

Active sample jobs: `example-company-policy-officer` (synthetic) and `green-european-foundation-policy-consultant-on-green-transition` (real capture). Live dashboard: [GitHub Pages](https://brickwalllegend2000.github.io/jobbrainmine/).

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
