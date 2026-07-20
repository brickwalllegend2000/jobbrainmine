"""Tests for Brainjob integrity checks."""

from brainjob.integrity import (
    compute_sha256,
    stamp_description_original,
    verify_description_original,
)


def test_compute_sha256_is_deterministic():
    content = "The complete job description is pasted here exactly as published."
    expected = "d64e54f894b3d017c37d80456a6bcd4fb1a5536a7a5cf51447718ae227347bd8"
    assert compute_sha256(content) == expected


def test_verify_description_original_passes_with_matching_hash():
    job = {
        "description_original": {
            "content": "hello",
            "sha256": compute_sha256("hello"),
        }
    }
    valid, error = verify_description_original(job)
    assert valid is True
    assert error is None


def test_verify_description_original_fails_on_tampered_content():
    job = {
        "description_original": {
            "content": "tampered",
            "sha256": compute_sha256("original"),
        }
    }
    valid, error = verify_description_original(job)
    assert valid is False
    assert "integrity mismatch" in (error or "")


def test_stamp_description_original_sets_hash_without_mutating_input():
    original = {"content": "preserve me", "sha256": "old"}
    stamped = stamp_description_original(original)
    assert original["sha256"] == "old"
    assert stamped["sha256"] == compute_sha256("preserve me")
