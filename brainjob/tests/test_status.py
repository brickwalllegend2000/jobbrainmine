"""Tests for brainjob status summary."""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

from brainjob.cli import main
from brainjob.status import format_status, status_workspace


def _write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def test_status_empty_workspace(tmp_path: Path):
    root = tmp_path / "workspace"
    (root / "data" / "jobs").mkdir(parents=True)
    (root / "tracking").mkdir()

    report = status_workspace(root)
    assert report.job_count == 0
    assert report.by_status == {}
    assert report.overdue_next_actions == 0
    assert "Jobs: 0" in format_status(report)
    assert main(["--root", str(root), "status"]) == 0


def test_status_counts_example_job(workspace_root: Path, tmp_path: Path):
    root = tmp_path / "workspace"
    (root / "data" / "jobs").mkdir(parents=True)
    (root / "tracking").mkdir()
    src = workspace_root / "data" / "jobs" / "example-company-policy-officer"
    shutil.copytree(src, root / "data" / "jobs" / "example-company-policy-officer")

    report = status_workspace(root, today=date(2026, 7, 20))
    assert report.job_count == 1
    assert report.by_status == {"preparing": 1}
    assert report.upcoming_deadlines == 1
    assert report.overdue_next_actions == 0
    assert any(action.job_id == "example-company-policy-officer" for action in report.next_actions)
    assert main(["--root", str(root), "status"]) == 0


def test_status_detects_overdue_next_action(workspace_root: Path, tmp_path: Path):
    root = tmp_path / "workspace"
    (root / "data" / "jobs").mkdir(parents=True)
    (root / "tracking").mkdir()
    src = workspace_root / "data" / "jobs" / "example-company-policy-officer"
    dest = root / "data" / "jobs" / "example-company-policy-officer"
    shutil.copytree(src, dest)

    application_path = dest / "application.json"
    application = json.loads(application_path.read_text(encoding="utf-8"))
    application["next_action"] = {
        "description": "Send follow-up",
        "due": "2020-01-01",
        "completed": False,
    }
    _write_json(application_path, application)

    report = status_workspace(root, today=date(2026, 7, 20))
    assert report.overdue_next_actions >= 1
    assert any(action.overdue for action in report.next_actions)
    assert main(["--root", str(root), "status"]) == 0


def test_status_invalid_json_exits_one(workspace_root: Path, tmp_path: Path):
    root = tmp_path / "workspace"
    (root / "data" / "jobs").mkdir(parents=True)
    (root / "tracking").mkdir()
    src = workspace_root / "data" / "jobs" / "example-company-policy-officer"
    dest = root / "data" / "jobs" / "broken-job"
    shutil.copytree(src, dest)
    (dest / "job.json").write_text("{not-json", encoding="utf-8")

    assert main(["--root", str(root), "status"]) == 1
