"""Generate tracking/index.json and dashboard.html from authoritative job data."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from brainjob.io import load_json, save_json
from brainjob.integrity import verify_description_original
from brainjob.paths import dashboard_path, index_path, iter_active_job_dirs, tracking_dir
from brainjob.validate import validate_workspace


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _is_overdue(due: str | None, completed: bool) -> bool:
    if completed or not due:
        return False
    due_date = _parse_date(due)
    if due_date is None:
        return False
    return due_date < date.today()


def _load_job_bundle(job_path: Path) -> dict[str, Any]:
    job_id = job_path.name
    return {
        "job": load_json(job_path / "job.json"),
        "application": load_json(job_path / "application.json"),
        "contacts": load_json(job_path / "contacts.json"),
        "notes": load_json(job_path / "notes.json"),
        "documents": load_json(job_path / "documents.json"),
        "job_id": job_id,
    }


def build_index_entry(bundle: dict[str, Any]) -> dict[str, Any]:
    job = bundle["job"]
    application = bundle["application"]
    contacts = bundle["contacts"]
    notes = bundle["notes"]
    documents = bundle["documents"]
    job_id = bundle["job_id"]

    integrity_valid, integrity_error = verify_description_original(job)
    next_action = application.get("next_action")
    overdue = False
    if isinstance(next_action, dict):
        overdue = _is_overdue(next_action.get("due"), bool(next_action.get("completed")))

    submitted_docs = sum(
        1 for doc in documents.get("documents", []) if doc.get("submitted") is True
    )
    pending_docs = sum(
        1 for doc in documents.get("documents", []) if doc.get("submitted") is False
    )

    return {
        "id": job_id,
        "role": job.get("role", {}),
        "location": job.get("location", {}),
        "compensation": job.get("compensation", {}),
        "dates": job.get("dates", {}),
        "source": job.get("source", {}),
        "classification": job.get("classification", {}),
        "description_original": {
            "format": job.get("description_original", {}).get("format"),
            "content": job.get("description_original", {}).get("content"),
            "language": job.get("description_original", {}).get("language"),
            "captured_at": job.get("description_original", {}).get("captured_at"),
            "sha256": job.get("description_original", {}).get("sha256"),
        },
        "integrity": {
            "valid": integrity_valid,
            "sha256": job.get("description_original", {}).get("sha256"),
            "error": integrity_error,
        },
        "application": {
            "status": application.get("status"),
            "saved_date": application.get("saved_date"),
            "applied_date": application.get("applied_date"),
            "next_action": next_action,
            "overdue_action": overdue,
            "timeline": application.get("timeline", []),
            "interviews": application.get("interviews", []),
            "assessments": application.get("assessments", []),
            "offer": application.get("offer"),
            "outcome": application.get("outcome"),
        },
        "contacts": contacts.get("contacts", []),
        "notes": notes.get("notes", []),
        "documents": {
            "items": documents.get("documents", []),
            "submitted_count": submitted_docs,
            "pending_count": pending_docs,
        },
        "data_path": f"../data/jobs/{job_id}",
    }


def build_index(root: Path) -> dict[str, Any]:
    jobs: list[dict[str, Any]] = []
    status_counts: dict[str, int] = {}
    overdue_actions = 0
    upcoming_deadlines = 0
    today = date.today()

    for job_path in iter_active_job_dirs(root):
        bundle = _load_job_bundle(job_path)
        entry = build_index_entry(bundle)
        jobs.append(entry)

        status = entry["application"]["status"] or "unknown"
        status_counts[status] = status_counts.get(status, 0) + 1

        if entry["application"]["overdue_action"]:
            overdue_actions += 1

        deadline = _parse_date(entry["dates"].get("deadline"))
        if deadline and deadline >= today:
            upcoming_deadlines += 1

    generated_at = datetime.now().astimezone().isoformat(timespec="seconds")
    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "stats": {
            "total_jobs": len(jobs),
            "by_status": status_counts,
            "overdue_actions": overdue_actions,
            "upcoming_deadlines": upcoming_deadlines,
        },
        "jobs": jobs,
    }


def render_dashboard(index_data: dict[str, Any]) -> str:
    assets_css = (Path(__file__).parent / "dashboard.css").read_text(encoding="utf-8")
    assets_js = (Path(__file__).parent / "dashboard.js").read_text(encoding="utf-8")
    payload = json.dumps(index_data, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Brainjob Dashboard</title>
  <style>
{assets_css}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <h1>Brainjob</h1>
      <p class="subtitle">JSON-only job search tracker</p>
    </div>
  </header>
  <main class="wrap">
    <section id="stats-panel" class="panel"></section>
    <section id="filters-panel" class="panel">
      <div class="filters">
        <label>
          Status
          <select id="filter-status">
            <option value="">All statuses</option>
          </select>
        </label>
        <label>
          Priority
          <select id="filter-priority">
            <option value="">All priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </label>
        <label class="checkbox">
          <input type="checkbox" id="filter-overdue"> Overdue actions only
        </label>
        <label class="checkbox">
          <input type="checkbox" id="filter-integrity"> Integrity issues only
        </label>
        <input type="search" id="filter-search" placeholder="Search title, company, tags">
      </div>
    </section>
    <section id="jobs-panel" class="panel"></section>
    <section id="detail-panel" class="panel hidden">
      <button type="button" id="detail-close" class="btn-secondary">Close detail</button>
      <div id="detail-content"></div>
    </section>
  </main>
  <footer class="site-footer wrap">
    <p>Generated at <span id="generated-at"></span>. Authoritative data lives under <code>data/jobs/</code>.</p>
  </footer>
  <script id="brainjob-data" type="application/json">{payload}</script>
  <script>
{assets_js}
  </script>
</body>
</html>
"""


def sync_workspace(root: Path, *, check_only: bool = False) -> tuple[bool, str]:
    report = validate_workspace(root)
    if not report.ok:
        return False, f"Sync aborted: validation failed with {report.total_errors} error(s)."

    index_data = build_index(root)
    index_file = index_path(root)
    dashboard_file = dashboard_path(root)

    if check_only:
        if not index_file.is_file():
            return False, "tracking/index.json is missing (run brainjob sync)."
        existing = load_json(index_file)
        if existing == index_data:
            return True, "tracking/index.json is up to date."
        return False, "tracking/index.json is stale (run brainjob sync)."

    tracking_dir(root).mkdir(parents=True, exist_ok=True)
    save_json(index_file, index_data)
    dashboard_file.write_text(render_dashboard(index_data), encoding="utf-8")
    return True, f"Synced {index_data['stats']['total_jobs']} job(s) to tracking/."
