"""CLI smoke tests."""

from pathlib import Path

from brainjob.cli import main


def test_cli_validate_and_sync(workspace_root: Path):
    assert main(["--root", str(workspace_root), "validate"]) == 0
    assert main(["--root", str(workspace_root), "sync"]) == 0
    assert main(["--root", str(workspace_root), "sync", "--check"]) == 0


def test_cli_add(workspace_root: Path, tmp_path: Path):
    root = tmp_path / "workspace"
    (root / "data" / "jobs").mkdir(parents=True)
    (root / "tracking").mkdir()
    templates = workspace_root / "data" / "templates" / "job"
    target_templates = root / "data" / "templates" / "job"
    target_templates.mkdir(parents=True)
    for path in templates.glob("*.json"):
        target_templates.joinpath(path.name).write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

    code = main(
        [
            "--root",
            str(root),
            "add",
            "--title",
            "Engineer",
            "--company",
            "CLI Co",
            "--description",
            "CLI created job description.",
            "--url",
            "https://cli.example/jobs/engineer",
        ]
    )
    assert code == 0
    assert any((root / "data" / "jobs").iterdir())
