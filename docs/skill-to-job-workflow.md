# Skill to job workflow

End-to-end flow: paste or scrape a vacancy posting, clean it with the formatter skill, create a Brainjob record with `brainjob add`, then validate and sync.

## Prerequisites

```bash
cd brainjob
python -m pip install -e ".[dev]"
```

Run CLI commands from `brainjob/` (or set `BRAINJOB_ROOT` / pass `--root`).

## Skills involved

| Skill | Path | Role |
|-------|------|------|
| extracted-output-formatter | [`skills/extracted-output-formatter/`](../skills/extracted-output-formatter/) | Clean messy extracted text without losing information |
| brainjob-add-job | [`skills/brainjob-add-job/`](../skills/brainjob-add-job/) | Map fields and create a job via `brainjob add` |

## Step-by-step

1. **Capture raw text** -- Paste the posting, OCR output, or scrape into the agent chat (or a scratch file).
2. **Clean with the formatter** -- Invoke `extracted-output-formatter`. Preserve the full original body; only restructure and normalize (dates to ISO `YYYY-MM-DD`, consistent spacing, clear field labels).
3. **Confirm mapped fields** -- Require at least title, company, description (full posting), and source URL. Confirm before add when any of those are ambiguous.
4. **Create the job** -- From `brainjob/`:

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
  --tags policy eu-affairs
```

Field map details: [`skills/brainjob-add-job/references/field-map.md`](../skills/brainjob-add-job/references/field-map.md).

5. **Optional hand-edits** -- Update `application.json`, `contacts.json`, `notes.json`, or `documents.json` under `data/jobs/<job-id>/`. Do not rewrite `description_original.content` in `job.json` after capture. Put AI commentary in `notes.json` with `"author": "ai"`.
6. **Validate and sync**:

```bash
brainjob validate
brainjob sync
```

7. **View the dashboard** -- Local: `python -m http.server 8000 --directory tracking` then open `http://localhost:8000/dashboard.html`. Live: [GitHub Pages](https://brickwalllegend2000.github.io/jobbrainmine/).

## Load adapters by tool

Canonical content lives under `skills/<skill-name>/`. Edit those files first; adapters are thin wrappers.

| Tool | How to load |
|------|-------------|
| **GitHub Copilot** | Skills under `.github/skills/` are picked up in Copilot-enabled repos. Adapters also live at `skills/<skill>/adapters/github-copilot/SKILL.md`. |
| **Cursor / generic agent** | Point the agent at `skills/<skill>/SKILL.md`, or paste `skills/<skill>/adapters/generic-agent/PROMPT.md` into agent instructions. |
| **Claude** | Paste `skills/<skill>/adapters/claude/PROMPT.md` into a Claude Project custom instruction (or Skills). Attach or link the canonical `SKILL.md` as project knowledge. |
| **ChatGPT** | Paste `skills/<skill>/adapters/chatgpt/PROMPT.md` into a Custom GPT or Project instruction. Upload or paste the canonical `SKILL.md` as knowledge. |

Both skills ship Claude and ChatGPT adapters:

- Formatter: `skills/extracted-output-formatter/adapters/{claude,chatgpt}/PROMPT.md`
- Add-job: `skills/brainjob-add-job/adapters/{claude,chatgpt}/PROMPT.md`

## Immutability reminders

1. `description_original.content` is employer content: stamp once at add, verify with SHA-256, never rewrite via tooling.
2. Personal and AI notes belong in `notes.json`.
3. `tracking/` is generated; `data/jobs/` is the source of truth.
