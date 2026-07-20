"""Filesystem layout helpers for a Brainjob workspace."""

from __future__ import annotations

import os
from pathlib import Path

JOB_FILES = (
    "job.json",
    "application.json",
    "contacts.json",
    "notes.json",
    "documents.json",
)


def find_root(start: Path | None = None) -> Path:
    """Walk upward from *start* (or cwd) to locate the Brainjob root."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "data" / "jobs").is_dir() and (candidate / "tracking").is_dir():
            return candidate
    raise FileNotFoundError(
        "Brainjob root not found. Run commands from inside a brainjob/ workspace "
        "(must contain data/jobs/ and tracking/)."
    )


def jobs_dir(root: Path) -> Path:
    return root / "data" / "jobs"


def templates_dir(root: Path) -> Path:
    return root / "data" / "templates" / "job"


def tracking_dir(root: Path) -> Path:
    return root / "tracking"


def index_path(root: Path) -> Path:
    return tracking_dir(root) / "index.json"


def dashboard_path(root: Path) -> Path:
    return tracking_dir(root) / "dashboard.html"


def archive_dir(root: Path) -> Path:
    return jobs_dir(root) / "_archive"


def job_dir(root: Path, job_id: str) -> Path:
    return jobs_dir(root) / job_id


def iter_active_job_dirs(root: Path) -> list[Path]:
    """Return sorted job directories, excluding archive and hidden paths."""
    base = jobs_dir(root)
    if not base.is_dir():
        return []
    dirs: list[Path] = []
    for entry in sorted(base.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("_") or entry.name.startswith("."):
            continue
        dirs.append(entry)
    return dirs


def slugify(text: str) -> str:
    """Create a filesystem-safe job id from arbitrary text."""
    slug = text.lower().strip()
    for old, new in ((" ", "-"), ("_", "-"), ("/", "-"), ("\\", "-")):
        slug = slug.replace(old, new)
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
    slug = "".join(ch if ch in allowed else "-" for ch in slug)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "job"


def resolve_root(explicit: str | None = None) -> Path:
    if explicit:
        return find_root(Path(explicit))
    env = os.environ.get("BRAINJOB_ROOT")
    if env:
        return find_root(Path(env))
    return find_root()
