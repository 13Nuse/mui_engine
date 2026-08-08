"""
backend/helpers/json_loader.py

JSON loading helpers for backend data models.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def load_json(path: Path | str) -> Any:
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_json_list(path: Path | str) -> list[dict[str, Any]]:
    raw = load_json(path)
    if not isinstance(raw, list):
        raise ValueError("JSON file must contain a top-level list of objects")
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise ValueError(f"Entry at index {index} must be a JSON object")
    return raw


def load_objects_from_json(path: Path | str, factory: Callable[[dict[str, Any]], T]) -> list[T]:
    return [factory(entry) for entry in load_json_list(path)]


def enum_from_name(enum_class: type, value: str, default: str | None = None):
    if value is None:
        if default is None:
            raise ValueError(f"Missing value for enum {enum_class.__name__}")
        value = default

    try:
        return enum_class[value.upper()]
    except KeyError as exc:
        raise ValueError(f"Unknown {enum_class.__name__} value: {value}") from exc
