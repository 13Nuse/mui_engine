"""
backend/items/models.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from core.settings import ItemType, ItemRarity, EquipSlot


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

@dataclass(frozen=True, slots=True)
class Item:
    """
    A read-only definition of an item. Two players carrying "Potion"
    both reference conceptually the same Item; only the quantity differs,
    which is tracked separately in an InventorySlot.
    """

    item_id: str
    name: str
    description: str
    item_type: ItemType
    rarity: ItemRarity = ItemRarity.COMMON
    equip_slot: EquipSlot = EquipSlot.NONE

    buy_price: int = 0
    sell_price: int = 0
    stackable: bool = True
    max_stack: int = 99

    stat_modifiers: StatModifiers = field(default_factory=StatModifiers)

    # consumable-specific
    restores_hp: int = 0
    restores_mp: int = 0
    cures_status: tuple[str, ...] = field(default_factory=tuple)

    # sprite lookup key - frontend resolves this to an actual surface
    icon_key: Optional[str] = None

    def is_usable_in_field(self) -> bool:
        return self.item_type == ItemType.CONSUMABLE

    def is_usable_in_battle(self) -> bool:
        return self.item_type in (ItemType.CONSUMABLE,) # will add more into the list when created

    def is_equippable(self) -> bool:
        return self.equip_slot != EquipSlot.NONE