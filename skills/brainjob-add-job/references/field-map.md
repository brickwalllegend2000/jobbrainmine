# Field map: extracted posting → `brainjob add`

Map cleaned extract fields to CLI flags. Run from the `brainjob/` directory (or set `BRAINJOB_ROOT` / `--root`).

| Extracted field | CLI flag | Required | Notes |
|-----------------|----------|----------|-------|
| Job title / role | `--title` | Yes | Exact role name from the posting |
| Employer / organization | `--company` | Yes | |
| Full original posting body | `--description` | Yes | Immutable after capture; preserve all text |
| Source / apply URL | `--url` | Yes | Prefer the canonical vacancy URL |
| Directory slug override | `--job-id` | No | Default: slugified `company-title` |
| Team / unit | `--department` | No | |
| Location display string | `--location` | No | e.g. `Brussels, Belgium` |
| City | `--city` | No | |
| Country | `--country` | No | |
| Application deadline | `--deadline` | No | ISO date `YYYY-MM-DD` |
| Classification tags | `--tags` | No | Space-separated list (`nargs=*`) |
| Priority | `--priority` | No | `low`, `medium` (default), or `high` |

## Example command

```bash
brainjob add \
  --title "Policy Officer" \
  --company "Example Company" \
  --description "Paste the full original posting here." \
  --url "https://example.com/jobs/policy-officer" \
  --location "Brussels, Belgium" \
  --city Brussels \
  --country Belgium \
  --deadline 2026-08-15 \
  --tags policy eu-affairs \
  --priority medium
```

## After add

| Step | Command / action |
|------|------------------|
| Hand-edit status, contacts, notes, documents | Edit JSON under `data/jobs/<job-id>/` |
| AI notes | `notes.json` entries with `"author": "ai"` |
| Validate | `brainjob validate` |
| Regenerate dashboard | `brainjob sync` |

Do not rewrite `description_original.content` in `job.json` after the job is created.
