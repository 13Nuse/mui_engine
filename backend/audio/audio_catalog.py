"""
backend/audio/audio_catalog.py
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SFXCatalog:
    paths: dict[str, str] = field(default_factory=dict)

    def register(self) -> None:
        ...

    def get(self) -> None:
        ...


@dataclass
class BGMCatalog:
    tracks: dict[str, str] = field(default_factory=dict)

    def register(self) -> None:
            ...
    
    def get(self) -> None:
        ...
    
