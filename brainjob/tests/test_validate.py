"""Validation tests."""

from pathlib import Path

import pytest

from brainjob.schemas import validate_job_directory
from brainjob.validate import validate_workspace


@pytest.fixture
def workspace_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_example_job_validates(workspace_root: Path):
    report = validate_workspace(workspace_root)
    assert report.ok, report.job_errors


def test_tampered_description_fails_validation(workspace_root: Path, tmp_path: Path):
    job_path = workspace_root / "data" / "jobs" / "example-company-policy-officer"
    target = tmp_path / "example-company-policy-officer"
    target.mkdir()
    for filename in ("job.json", "application.json", "contacts.json", "notes.json", "documents.json"):
        (target / filename).write_text((job_path / filename).read_text(encoding="utf-8"), encoding="utf-8")

    job_file = target / "job.json"
    text = job_file.read_text(encoding="utf-8")
    job_file.write_text(text.replace("exactly as published.", "changed text."), encoding="utf-8")

    errors = validate_job_directory(target)
    assert any("integrity mismatch" in error for error in errors)
