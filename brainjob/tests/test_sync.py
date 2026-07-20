"""Sync command tests."""

from pathlib import Path

from brainjob.io import load_json
from brainjob.sync import sync_workspace


def test_sync_generates_index_and_dashboard(workspace_root: Path):
    ok, message = sync_workspace(workspace_root)
    assert ok, message

    index_path = workspace_root / "tracking" / "index.json"
    dashboard_path = workspace_root / "tracking" / "dashboard.html"

    assert index_path.is_file()
    assert dashboard_path.is_file()

    index = load_json(index_path)
    assert index["schema_version"] == 1
    assert index["stats"]["total_jobs"] >= 1
    assert any(job["id"] == "example-company-policy-officer" for job in index["jobs"])

    html = dashboard_path.read_text(encoding="utf-8")
    assert "Brainjob Dashboard" in html
    assert "example-company-policy-officer" in html


def test_sync_check_detects_stale_index(workspace_root: Path):
    sync_workspace(workspace_root)
    ok, _ = sync_workspace(workspace_root, check_only=True)
    assert ok is True

    index_path = workspace_root / "tracking" / "index.json"
    index = load_json(index_path)
    index["stats"]["total_jobs"] = 999
    index_path.write_text(__import__("json").dumps(index), encoding="utf-8")

    ok, message = sync_workspace(workspace_root, check_only=True)
    assert ok is False
    assert "stale" in message


def test_sync_check_ignores_generated_at(workspace_root: Path):
    sync_workspace(workspace_root)
    index_path = workspace_root / "tracking" / "index.json"
    index = load_json(index_path)
    index["generated_at"] = "2000-01-01T00:00:00+00:00"
    index_path.write_text(
        __import__("json").dumps(index, indent=2) + "\n",
        encoding="utf-8",
    )

    ok, message = sync_workspace(workspace_root, check_only=True)
    assert ok is True, message
