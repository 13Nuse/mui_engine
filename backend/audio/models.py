"""
backend/audio/models.py
"""
from __future__ import annotations

from enum import Enum, auto


class SFXEvent(Enum):
    # menu
    MENU_CURSOR = auto()
    MENU_CONFIRM = auto()
    MENU_CANCEL = auto()
    MENU_ERROR = auto()

    # battle
    BATTLE_HIT = auto()
    BATTLE_MISS = auto()
    BATTLE_DEFEND = auto()
    BATTLE_ITEM_USE = auto()
    BATTLE_ENEMY_DEFEATED = auto()
    BATTLE_ALLY_DOWN = auto()
    BATTLE_FLEE_SUCCESS = auto()
    BATTLE_FLEE_FAIL = auto()
    BATTLE_VICTORY = auto()
    BATTLE_DEFEAT = auto()
    BATTLE_LEVEL_UP = auto()

    # shop
    SHOP_BUY = auto()
    SHOP_SELL = auto()
    SHOP_ERROR = auto()

    # overworld
    WARP = auto()
    CHEST_OPEN = auto()