"""Create new job directories from templates."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from brainjob.integrity import stamp_description_original
from brainjob.io import load_json, save_json
from brainjob.paths import iter_active_job_dirs, job_dir, slugify, templates_dir


def _null_if_empty(value: str) -> str | None:
    return value if value else None


def _now_iso(tz_name: str = "Europe/Brussels") -> str:
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = timezone.utc
    return datetime.now(tz).isoformat(timespec="seconds")


def _today_iso(tz_name: str = "Europe/Brussels") -> str:
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = timezone.utc
    return datetime.now(tz).date().isoformat()


def _render_template(template: dict[str, Any], replacements: dict[str, str]) -> dict[str, Any]:
    text = json.dumps(template)
    for key, value in replacements.items():
        # Placeholders sit inside JSON strings; escape so newlines/quotes stay valid.
        escaped = json.dumps(value)[1:-1]
        text = text.replace(f"{{{{{key}}}}}", escaped)
    return json.loads(text)


def suggest_job_id(company: str, title: str, root: Path) -> str:
    base = slugify(f"{company}-{title}")
    existing = {path.name for path in iter_active_job_dirs(root)}
    if base not in existing:
        return base
    suffix = 2
    while f"{base}-{suffix}" in existing:
        suffix += 1
    return f"{base}-{suffix}"


def add_job(
    root: Path,
    *,
    title: str,
    company: str,
    description: str,
    url: str,
    job_id: str | None = None,
    department: str | None = None,
    location_display: str | None = None,
    city: str | None = None,
    country: str | None = None,
    deadline: str | None = None,
    tags: list[str] | None = None,
    priority: str = "medium",
    timezone: str = "Europe/Brussels",
) -> str:
    templates = templates_dir(root)
    if not templates.is_dir():
        raise FileNotFoundError(f"Templates not found at {templates}")

    resolved_id = job_id or suggest_job_id(company, title, root)
    target = job_dir(root, resolved_id)
    if target.exists():
        raise FileExistsError(f"Job directory already exists: {target}")

    now = _now_iso(timezone)
    today = _today_iso(timezone)
    domain = ""
    if "://" in url:
        domain = url.split("://", 1)[1].split("/", 1)[0]

    replacements = {
        "JOB_ID": resolved_id,
        "TITLE": title,
        "COMPANY": company,
        "DEPARTMENT": department or "",
        "LOCATION_DISPLAY": location_display or "",
        "CITY": city or "",
        "COUNTRY": country or "",
        "URL": url,
        "DOMAIN": domain,
        "DEADLINE": deadline or "",
        "DESCRIPTION": description,
        "CAPTURED_AT": now,
        "SAVED_DATE": today,
        "TIMESTAMP": now,
        "PRIORITY": priority,
    }

    job_template = load_json(templates / "job.json")
    job_data = _render_template(job_template, replacements)
    if tags:
        job_data["classification"]["tags"] = tags
    job_data["role"]["department"] = _null_if_empty(job_data["role"].get("department"))
    job_data["location"]["display"] = location_display or job_data["location"].get("display") or None
    job_data["location"]["city"] = _null_if_empty(job_data["location"].get("city"))
    job_data["location"]["country"] = _null_if_empty(job_data["location"].get("country"))
    job_data["dates"]["deadline"] = _null_if_empty(job_data["dates"].get("deadline") or "")
    job_data["description_original"] = stamp_description_original(
        job_data["description_original"]
    )

    companion: list[tuple[str, dict[str, Any]]] = []
    for filename in ("application.json", "contacts.json", "notes.json", "documents.json"):
        template = load_json(templates / filename)
        companion.append((filename, _render_template(template, replacements)))

    target.mkdir(parents=True)
    save_json(target / "job.json", job_data)
    for filename, data in companion:
        save_json(target / filename, data)

    return resolved_id
