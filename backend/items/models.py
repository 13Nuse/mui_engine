"""
backend/items/models.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class ItemType(Enum):
    CONSUMABLE = auto()
    WEAPON = auto()
    ARMOR = auto()
    ACCESSORY = auto()
    KEY_ITEM = auto()
    MATERIAL = auto()


class ItemRarity(Enum):
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto ()
    EPIC = auto()
    lEGENDARY = auto()


@dataclass(frozen=True, slots=True)
class StatModifiers:
    """Stat bonus an item can grant when equipped or restore when consumed."""

    hp: int = 0
    mana: int = 0
    attack: int = 0
    magic_attack: int = 0
    defence: int = 0
    magic_defence: int = 0
    speed: int = 0
    resistance: int = 0
    hp: int = 0 # will fill the rest out later
    hp: int = 0
    hp: int = 0
    hp: int = 0
    hp: int = 0