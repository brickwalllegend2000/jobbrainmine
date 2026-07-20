"""Content integrity for immutable employer descriptions."""

from __future__ import annotations

import hashlib
from typing import Any


def compute_sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def verify_description_original(job: dict[str, Any]) -> tuple[bool, str | None]:
    """Return (valid, error_message). Never mutates *job*."""
    desc = job.get("description_original")
    if not isinstance(desc, dict):
        return False, "job.json missing description_original object"
    content = desc.get("content")
    stored = desc.get("sha256")
    if not isinstance(content, str):
        return False, "description_original.content must be a string"
    if not isinstance(stored, str) or not stored:
        return False, "description_original.sha256 must be a non-empty string"
    expected = compute_sha256(content)
    if stored != expected:
        return False, (
            f"description_original integrity mismatch: stored sha256={stored!r}, "
            f"computed sha256={expected!r}"
        )
    return True, None


def stamp_description_original(desc: dict[str, Any]) -> dict[str, Any]:
    """Return a copy with sha256 set from content (for new captures only)."""
    result = dict(desc)
    content = result.get("content", "")
    if not isinstance(content, str):
        content = str(content)
    result["content"] = content
    result["sha256"] = compute_sha256(content)
    return result
