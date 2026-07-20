"""Archive completed or inactive job records."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from brainjob.io import load_json, save_json
from brainjob.paths import archive_dir, job_dir


def archive_job(root: Path, job_id: str) -> str:
    source = job_dir(root, job_id)
    if not source.is_dir():
        raise FileNotFoundError(f"Job not found: {job_id}")

    destination_root = archive_dir(root)
    destination_root.mkdir(parents=True, exist_ok=True)
    destination = destination_root / job_id
    if destination.exists():
        raise FileExistsError(f"Archived job already exists: {destination}")

    application_path = source / "application.json"
    application: dict[str, Any] = load_json(application_path)
    now = datetime.now().astimezone().isoformat(timespec="seconds")

    application["status"] = "archived"
    timeline = list(application.get("timeline", []))
    timeline.append(
        {
            "timestamp": now,
            "type": "archived",
            "description": "Job archived in Brainjob",
        }
    )
    application["timeline"] = timeline
    save_json(application_path, application)

    source.rename(destination)
    return f"Archived {job_id} to data/jobs/_archive/{job_id}"
