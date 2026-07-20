"""JSON schema validation for Brainjob files."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

from brainjob.integrity import verify_description_original

APPLICATION_STATUSES = frozenset(
    {
        "saved",
        "preparing",
        "applied",
        "interviewing",
        "assessment",
        "offer",
        "accepted",
        "rejected",
        "withdrawn",
        "archived",
    }
)

NOTE_AUTHORS = frozenset({"user", "ai"})
NOTE_CATEGORIES = frozenset(
    {"research", "strategy", "interview-prep", "follow-up", "general"}
)
DOCUMENT_TYPES = frozenset({"cv", "cover_letter", "portfolio", "other"})
POSTING_STATUSES = frozenset({"open", "closed", "unknown"})
PRIORITIES = frozenset({"low", "medium", "high"})
WORK_ARRANGEMENTS = frozenset({"on-site", "hybrid", "remote", "unknown"})
CAPTURE_METHODS = frozenset({"manual", "import", "scrape"})


class ValidationError(Exception):
    def __init__(self, path: str, message: str) -> None:
        self.path = path
        self.message = message
        super().__init__(f"{path}: {message}")


def _require(obj: dict[str, Any], key: str, path: str) -> Any:
    if key not in obj:
        raise ValidationError(path, f"missing required field {key!r}")
    return obj[key]


def _optional_string(value: Any, path: str) -> None:
    if value is not None and not isinstance(value, str):
        raise ValidationError(path, "must be a string or null")


def _optional_date(value: Any, path: str) -> None:
    if value is None:
        return
    if not isinstance(value, str):
        raise ValidationError(path, "must be an ISO date string or null")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(path, f"invalid date: {exc}") from exc


def _optional_datetime(value: Any, path: str) -> None:
    if value is None:
        return
    if not isinstance(value, str):
        raise ValidationError(path, "must be an ISO datetime string or null")
    try:
        datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(path, f"invalid datetime: {exc}") from exc


def _require_string(value: Any, path: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValidationError(path, "must be a non-empty string")


def _require_bool(value: Any, path: str) -> None:
    if not isinstance(value, bool):
        raise ValidationError(path, "must be a boolean")


def _require_list(value: Any, path: str) -> None:
    if not isinstance(value, list):
        raise ValidationError(path, "must be an array")


def validate_job(data: dict[str, Any], job_id: str | None = None) -> list[str]:
    errors: list[str] = []
    prefix = f"{job_id}/job.json" if job_id else "job.json"
    try:
        if data.get("schema_version") != 1:
            raise ValidationError(prefix, "schema_version must be 1")
        _require_string(_require(data, "id", prefix), f"{prefix}.id")
        if job_id and data["id"] != job_id:
            raise ValidationError(prefix, f"id {data['id']!r} does not match directory {job_id!r}")

        role = _require(data, "role", prefix)
        if not isinstance(role, dict):
            raise ValidationError(f"{prefix}.role", "must be an object")
        _require_string(_require(role, "title", f"{prefix}.role"), f"{prefix}.role.title")
        _require_string(_require(role, "company", f"{prefix}.role"), f"{prefix}.role.company")
        _optional_string(role.get("department"), f"{prefix}.role.department")
        _optional_string(role.get("employment_type"), f"{prefix}.role.employment_type")
        _optional_string(role.get("seniority"), f"{prefix}.role.seniority")

        location = _require(data, "location", prefix)
        if not isinstance(location, dict):
            raise ValidationError(f"{prefix}.location", "must be an object")
        _require_string(_require(location, "display", f"{prefix}.location"), f"{prefix}.location.display")

        compensation = _require(data, "compensation", prefix)
        if not isinstance(compensation, dict):
            raise ValidationError(f"{prefix}.compensation", "must be an object")

        dates = _require(data, "dates", prefix)
        if not isinstance(dates, dict):
            raise ValidationError(f"{prefix}.dates", "must be an object")
        _optional_date(dates.get("published"), f"{prefix}.dates.published")
        _optional_date(dates.get("deadline"), f"{prefix}.dates.deadline")
        _require_string(_require(dates, "captured", f"{prefix}.dates"), f"{prefix}.dates.captured")

        source = _require(data, "source", prefix)
        if not isinstance(source, dict):
            raise ValidationError(f"{prefix}.source", "must be an object")
        _require_string(_require(source, "url", f"{prefix}.source"), f"{prefix}.source.url")
        posting = source.get("posting_status")
        if posting is not None and posting not in POSTING_STATUSES:
            raise ValidationError(f"{prefix}.source.posting_status", f"must be one of {sorted(POSTING_STATUSES)}")

        desc = _require(data, "description_original", prefix)
        if not isinstance(desc, dict):
            raise ValidationError(f"{prefix}.description_original", "must be an object")
        _require_string(_require(desc, "content", f"{prefix}.description_original"), f"{prefix}.description_original.content")
        _require_string(_require(desc, "sha256", f"{prefix}.description_original"), f"{prefix}.description_original.sha256")

        classification = _require(data, "classification", prefix)
        if not isinstance(classification, dict):
            raise ValidationError(f"{prefix}.classification", "must be an object")
        tags = classification.get("tags")
        if tags is not None:
            _require_list(tags, f"{prefix}.classification.tags")
        priority = classification.get("priority")
        if priority is not None and priority not in PRIORITIES:
            raise ValidationError(f"{prefix}.classification.priority", f"must be one of {sorted(PRIORITIES)}")

        valid, msg = verify_description_original(data)
        if not valid:
            raise ValidationError(prefix, msg or "integrity check failed")
    except ValidationError as exc:
        errors.append(str(exc))
    return errors


def validate_application(data: dict[str, Any], job_id: str) -> list[str]:
    errors: list[str] = []
    prefix = f"{job_id}/application.json"
    try:
        _require_string(_require(data, "job_id", prefix), f"{prefix}.job_id")
        if data["job_id"] != job_id:
            raise ValidationError(prefix, f"job_id {data['job_id']!r} does not match directory {job_id!r}")
        status = _require(data, "status", prefix)
        if status not in APPLICATION_STATUSES:
            raise ValidationError(f"{prefix}.status", f"must be one of {sorted(APPLICATION_STATUSES)}")
        _optional_date(data.get("saved_date"), f"{prefix}.saved_date")
        _optional_date(data.get("applied_date"), f"{prefix}.applied_date")

        next_action = data.get("next_action")
        if next_action is not None:
            if not isinstance(next_action, dict):
                raise ValidationError(f"{prefix}.next_action", "must be an object or null")
            _require_bool(_require(next_action, "completed", f"{prefix}.next_action"), f"{prefix}.next_action.completed")

        timeline = _require(data, "timeline", prefix)
        _require_list(timeline, f"{prefix}.timeline")
        for index, event in enumerate(timeline):
            if not isinstance(event, dict):
                raise ValidationError(f"{prefix}.timeline[{index}]", "must be an object")
            _require_string(_require(event, "type", f"{prefix}.timeline[{index}]"), f"{prefix}.timeline[{index}].type")

        _require_list(_require(data, "interviews", prefix), f"{prefix}.interviews")
        _require_list(_require(data, "assessments", prefix), f"{prefix}.assessments")
    except ValidationError as exc:
        errors.append(str(exc))
    return errors


def validate_contacts(data: dict[str, Any], job_id: str) -> list[str]:
    errors: list[str] = []
    prefix = f"{job_id}/contacts.json"
    try:
        if data.get("job_id") != job_id:
            raise ValidationError(prefix, f"job_id must be {job_id!r}")
        contacts = _require(data, "contacts", prefix)
        _require_list(contacts, f"{prefix}.contacts")
        for index, contact in enumerate(contacts):
            cp = f"{prefix}.contacts[{index}]"
            if not isinstance(contact, dict):
                raise ValidationError(cp, "must be an object")
            _require_string(_require(contact, "name", cp), f"{cp}.name")
    except ValidationError as exc:
        errors.append(str(exc))
    return errors


def validate_notes(data: dict[str, Any], job_id: str) -> list[str]:
    errors: list[str] = []
    prefix = f"{job_id}/notes.json"
    try:
        if data.get("job_id") != job_id:
            raise ValidationError(prefix, f"job_id must be {job_id!r}")
        notes = _require(data, "notes", prefix)
        _require_list(notes, f"{prefix}.notes")
        for index, note in enumerate(notes):
            np = f"{prefix}.notes[{index}]"
            if not isinstance(note, dict):
                raise ValidationError(np, "must be an object")
            _require_string(_require(note, "id", np), f"{np}.id")
            _require_string(_require(note, "content", np), f"{np}.content")
            author = _require(note, "author", np)
            if author not in NOTE_AUTHORS:
                raise ValidationError(f"{np}.author", f"must be one of {sorted(NOTE_AUTHORS)}")
            category = note.get("category")
            if category is not None and category not in NOTE_CATEGORIES:
                raise ValidationError(f"{np}.category", f"must be one of {sorted(NOTE_CATEGORIES)}")
    except ValidationError as exc:
        errors.append(str(exc))
    return errors


def validate_documents(data: dict[str, Any], job_id: str) -> list[str]:
    errors: list[str] = []
    prefix = f"{job_id}/documents.json"
    try:
        if data.get("job_id") != job_id:
            raise ValidationError(prefix, f"job_id must be {job_id!r}")
        documents = _require(data, "documents", prefix)
        _require_list(documents, f"{prefix}.documents")
        for index, doc in enumerate(documents):
            dp = f"{prefix}.documents[{index}]"
            if not isinstance(doc, dict):
                raise ValidationError(dp, "must be an object")
            doc_type = _require(doc, "type", dp)
            if doc_type not in DOCUMENT_TYPES:
                raise ValidationError(f"{dp}.type", f"must be one of {sorted(DOCUMENT_TYPES)}")
            _require_string(_require(doc, "path", dp), f"{dp}.path")
            _require_bool(_require(doc, "submitted", dp), f"{dp}.submitted")
    except ValidationError as exc:
        errors.append(str(exc))
    return errors


def validate_job_directory(job_path: Path) -> list[str]:
    job_id = job_path.name
    errors: list[str] = []
    from brainjob.io import load_json

    for filename in ("job.json", "application.json", "contacts.json", "notes.json", "documents.json"):
        filepath = job_path / filename
        if not filepath.is_file():
            errors.append(f"{job_id}/{filename}: file not found")
            continue
        try:
            data = load_json(filepath)
        except Exception as exc:
            errors.append(f"{job_id}/{filename}: invalid JSON: {exc}")
            continue
        if filename == "job.json":
            errors.extend(validate_job(data, job_id))
        elif filename == "application.json":
            errors.extend(validate_application(data, job_id))
        elif filename == "contacts.json":
            errors.extend(validate_contacts(data, job_id))
        elif filename == "notes.json":
            errors.extend(validate_notes(data, job_id))
        elif filename == "documents.json":
            errors.extend(validate_documents(data, job_id))
    return errors
