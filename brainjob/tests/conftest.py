from pathlib import Path
import shutil

import pytest


@pytest.fixture
def workspace_root() -> Path:
    return Path(__file__).resolve().parents[1]


@pytest.fixture
def isolated_workspace(workspace_root: Path, tmp_path: Path) -> Path:
    """Copy job data into a temp workspace so tests never mutate tracking/."""
    root = tmp_path / "workspace"
    (root / "data" / "jobs").mkdir(parents=True)
    (root / "tracking").mkdir()

    src_jobs = workspace_root / "data" / "jobs"
    for job_dir in src_jobs.iterdir():
        if job_dir.is_dir() and not job_dir.name.startswith("_"):
            shutil.copytree(job_dir, root / "data" / "jobs" / job_dir.name)

    src_templates = workspace_root / "data" / "templates"
    if src_templates.is_dir():
        shutil.copytree(src_templates, root / "data" / "templates")

    return root
