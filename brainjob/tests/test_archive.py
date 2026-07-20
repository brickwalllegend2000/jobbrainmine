"""Archive command tests."""

from pathlib import Path

from brainjob.add import add_job
from brainjob.archive import archive_job
from brainjob.io import load_json
from brainjob.sync import sync_workspace


def _bootstrap_root(tmp_path: Path, templates_root: Path) -> Path:
    root = tmp_path / "workspace"
    (root / "data" / "jobs").mkdir(parents=True)
    (root / "tracking").mkdir()
    target_templates = root / "data" / "templates" / "job"
    target_templates.mkdir(parents=True)
    for path in (templates_root / "job").glob("*.json"):
        target_templates.joinpath(path.name).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return root


def test_archive_moves_job_and_sets_status(workspace_root: Path, tmp_path: Path):
    root = _bootstrap_root(tmp_path, workspace_root / "data" / "templates")
    job_id = add_job(
        root,
        title="Temp Role",
        company="Archive Inc",
        description="Original description for archive test.",
        url="https://archive.example/jobs/temp",
    )

    message = archive_job(root, job_id)
    assert "_archive" in message
    assert not (root / "data" / "jobs" / job_id).exists()
    assert (root / "data" / "jobs" / "_archive" / job_id).is_dir()

    application = load_json(root / "data" / "jobs" / "_archive" / job_id / "application.json")
    assert application["status"] == "archived"
    assert application["timeline"][-1]["type"] == "archived"

    ok, _ = sync_workspace(root)
    assert ok is True
    index = load_json(root / "tracking" / "index.json")
    assert index["stats"]["total_jobs"] == 0
