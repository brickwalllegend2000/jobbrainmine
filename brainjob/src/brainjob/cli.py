"""Brainjob command-line interface."""

from __future__ import annotations

import argparse
import sys

from brainjob import __version__
from brainjob.add import add_job
from brainjob.archive import archive_job
from brainjob.paths import resolve_root
from brainjob.status import format_status, status_workspace
from brainjob.sync import sync_workspace
from brainjob.validate import format_report, validate_workspace
from brainjob.watch import watch_workspace


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="brainjob",
        description="JSON-only job-search information system",
    )
    parser.add_argument(
        "--root",
        help="Brainjob workspace root (defaults to auto-detect or BRAINJOB_ROOT)",
    )
    parser.add_argument("--version", action="version", version=f"brainjob {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)

    add_cmd = sub.add_parser("add", help="Create a new job from templates")
    add_cmd.add_argument("--title", required=True)
    add_cmd.add_argument("--company", required=True)
    add_cmd.add_argument("--description", required=True, help="Original posting text")
    add_cmd.add_argument("--url", required=True)
    add_cmd.add_argument("--job-id")
    add_cmd.add_argument("--department")
    add_cmd.add_argument("--location")
    add_cmd.add_argument("--city")
    add_cmd.add_argument("--country")
    add_cmd.add_argument("--deadline", help="ISO date YYYY-MM-DD")
    add_cmd.add_argument("--tags", nargs="*", default=[])
    add_cmd.add_argument("--priority", choices=["low", "medium", "high"], default="medium")

    sub.add_parser("validate", help="Validate all job JSON files")

    sync_cmd = sub.add_parser("sync", help="Regenerate tracking/index.json and dashboard")
    sync_cmd.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if tracking/index.json is stale",
    )

    watch_cmd = sub.add_parser("watch", help="Watch data/jobs/ and sync on changes")
    watch_cmd.add_argument("--interval", type=float, default=2.0)

    archive_cmd = sub.add_parser("archive", help="Move a job to data/jobs/_archive/")
    archive_cmd.add_argument("job_id")

    sub.add_parser("status", help="Print a concise pipeline summary")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        root = resolve_root(args.root)
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    if args.command == "add":
        try:
            job_id = add_job(
                root,
                title=args.title,
                company=args.company,
                description=args.description,
                url=args.url,
                job_id=args.job_id,
                department=args.department,
                location_display=args.location,
                city=args.city,
                country=args.country,
                deadline=args.deadline,
                tags=args.tags,
                priority=args.priority,
            )
        except (FileExistsError, FileNotFoundError, ValueError) as exc:
            print(exc, file=sys.stderr)
            return 1
        print(f"Created job {job_id} at data/jobs/{job_id}/")
        return 0

    if args.command == "validate":
        report = validate_workspace(root)
        print(format_report(report))
        return 0 if report.ok else 1

    if args.command == "sync":
        ok, message = sync_workspace(root, check_only=args.check)
        print(message)
        return 0 if ok else 1

    if args.command == "watch":
        watch_workspace(root, interval=args.interval)
        return 0

    if args.command == "archive":
        try:
            message = archive_job(root, args.job_id)
        except (FileNotFoundError, FileExistsError) as exc:
            print(exc, file=sys.stderr)
            return 1
        print(message)
        return 0

    if args.command == "status":
        report = validate_workspace(root)
        if not report.ok:
            print(format_report(report))
            return 1
        print(format_status(status_workspace(root)))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
