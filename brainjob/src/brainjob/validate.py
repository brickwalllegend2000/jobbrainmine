"""Validate Brainjob workspaces and job records."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from brainjob.paths import iter_active_job_dirs
from brainjob.schemas import validate_job_directory


@dataclass
class ValidationReport:
    job_errors: dict[str, list[str]] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.job_errors

    @property
    def total_errors(self) -> int:
        return sum(len(items) for items in self.job_errors.values())


def validate_workspace(root: Path) -> ValidationReport:
    report = ValidationReport()
    for job_path in iter_active_job_dirs(root):
        errors = validate_job_directory(job_path)
        if errors:
            report.job_errors[job_path.name] = errors
    return report


def format_report(report: ValidationReport) -> str:
    if report.ok:
        return "Validation passed."
    lines = ["Validation failed:"]
    for job_id, errors in sorted(report.job_errors.items()):
        lines.append(f"  {job_id}:")
        for error in errors:
            lines.append(f"    - {error}")
    return "\n".join(lines)
