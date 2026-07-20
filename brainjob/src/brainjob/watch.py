"""Watch data/jobs/ and regenerate tracking artifacts."""

from __future__ import annotations

import time
from pathlib import Path

from brainjob.paths import jobs_dir
from brainjob.sync import sync_workspace


def _snapshot_jobs(root: Path) -> dict[str, float]:
    base = jobs_dir(root)
    snapshot: dict[str, float] = {}
    if not base.is_dir():
        return snapshot
    for path in base.rglob("*.json"):
        if "_archive" in path.parts:
            continue
        try:
            snapshot[str(path)] = path.stat().st_mtime
        except OSError:
            continue
    return snapshot


def watch_workspace(root: Path, *, interval: float = 2.0) -> None:
    print(f"Watching {jobs_dir(root)} (interval {interval}s). Press Ctrl+C to stop.")
    previous = _snapshot_jobs(root)
    ok, message = sync_workspace(root)
    print(message)
    try:
        while True:
            time.sleep(interval)
            current = _snapshot_jobs(root)
            if current != previous:
                previous = current
                ok, message = sync_workspace(root)
                print(message)
    except KeyboardInterrupt:
        print("\nStopped watching.")
