"""Add command tests."""

from pathlib import Path

from brainjob.add import add_job
from brainjob.schemas import validate_job_directory


def test_add_job_creates_valid_bundle(workspace_root: Path, tmp_path: Path):
    root = tmp_path / "workspace"
    (root / "data" / "jobs").mkdir(parents=True)
    (root / "tracking").mkdir()
    templates = workspace_root / "data" / "templates" / "job"
    target_templates = root / "data" / "templates" / "job"
    target_templates.mkdir(parents=True)
    for path in templates.glob("*.json"):
        target_templates.joinpath(path.name).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

    job_id = add_job(
        root,
        title="Analyst",
        company="Test Corp",
        description="Original posting text unchanged.",
        url="https://test.example/jobs/analyst",
        location_display="Remote",
        tags=["analysis"],
    )

    job_path = root / "data" / "jobs" / job_id
    assert job_path.is_dir()
    errors = validate_job_directory(job_path)
    assert errors == []
