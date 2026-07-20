"""JSON file I/O helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data: Any, *, indent: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=indent, ensure_ascii=False)
    text += "\n"
    with path.open("w", encoding="utf-8") as handle:
        handle.write(text)


def deep_copy(data: Any) -> Any:
    return json.loads(json.dumps(data))
