"""Workspace status summary for Brainjob."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from brainjob.io import load_json
from brainjob.paths import iter_active_job_dirs


@dataclass
class NextActionSummary:
    job_id: str
    description: str
    due: str | None
    overdue: bool


@dataclass
class StatusReport:
    job_count: int = 0
    by_status: dict[str, int] = field(default_factory=dict)
    overdue_next_actions: int = 0
    upcoming_deadlines: int = 0
    next_actions: list[NextActionSummary] = field(default_factory=list)


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _is_overdue(due: str | None, completed: bool) -> bool:
    if completed or not due:
        return False
    due_date = _parse_date(due)
    if due_date is None:
        return False
    return due_date < date.today()


def status_workspace(root: Path, *, today: date | None = None) -> StatusReport:
    """Summarize active jobs without writing tracking artifacts."""
    today = today or date.today()
    status_counts: Counter[str] = Counter()
    overdue_count = 0
    upcoming_deadlines = 0
    next_actions: list[NextActionSummary] = []
    job_count = 0

    for job_path in iter_active_job_dirs(root):
        job_count += 1
        job_id = job_path.name
        application: dict[str, Any] = load_json(job_path / "application.json")
        job: dict[str, Any] = load_json(job_path / "job.json")

        status = str(application.get("status") or "unknown")
        status_counts[status] += 1

        next_action = application.get("next_action")
        if isinstance(next_action, dict):
            completed = bool(next_action.get("completed"))
            due = next_action.get("due")
            due_str = due if isinstance(due, str) else None
            overdue = _is_overdue(due_str, completed)
            if overdue:
                overdue_count += 1
            if not completed:
                description = next_action.get("description") or "(no description)"
                next_actions.append(
                    NextActionSummary(
                        job_id=job_id,
                        description=str(description),
                        due=due_str,
                        overdue=overdue,
                    )
                )

        dates = job.get("dates") if isinstance(job.get("dates"), dict) else {}
        deadline = _parse_date(dates.get("deadline") if isinstance(dates, dict) else None)
        if deadline and deadline >= today:
            upcoming_deadlines += 1

    by_status = dict(sorted(status_counts.items()))
    next_actions.sort(key=lambda item: (item.due or "9999-99-99", item.job_id))
    return StatusReport(
        job_count=job_count,
        by_status=by_status,
        overdue_next_actions=overdue_count,
        upcoming_deadlines=upcoming_deadlines,
        next_actions=next_actions,
    )


def format_status(report: StatusReport) -> str:
    if report.by_status:
        by_status = ", ".join(f"{name}={count}" for name, count in report.by_status.items())
    else:
        by_status = "(none)"

    lines = [
        f"Jobs: {report.job_count}",
        f"By status: {by_status}",
        f"Overdue next actions: {report.overdue_next_actions}",
        f"Upcoming deadlines: {report.upcoming_deadlines}",
        "Next actions:",
    ]
    if not report.next_actions:
        lines.append("  (none)")
    else:
        for action in report.next_actions:
            due_part = f" (due {action.due})" if action.due else ""
            overdue_mark = " [overdue]" if action.overdue else ""
            lines.append(
                f"  - {action.job_id}: {action.description}{due_part}{overdue_mark}"
            )
    return "\n".join(lines)
