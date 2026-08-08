"""
backend/items/item_catalog.py

A simple in-memory registry mapping item_id -> Item definition. Loaded
once at startup, so any system (inventory, shop, battle) can look items up
by id without passing full Item objects around everywhere.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from backend.helpers.json_loader import enum_from_name, load_objects_from_json
from backend.items.models import EquipSlot, Item, ItemRarity, ItemType, StatModifiers


@dataclass
class ItemCatalog:
    items: dict[str, Item] = field(default_factory=dict)

    def register(self, item: Item) -> None:
        self.items[item.item_id] = item

    def get(self, item_id: str) -> Item:
        try:
            return self.items[item_id]
        except KeyError as exc:
            raise KeyError(f"Unknown item_id '{item_id}' in catalog") from exc

    def all(self) -> list[Item]:
        return list(self.items.values())


def _load_stat_modifiers(data: dict[str, Any]) -> StatModifiers:
    return StatModifiers(
        hp=data.get("hp", 0),
        mana=data.get("mana", 0),
        attack=data.get("attack", 0),
        magic_attack=data.get("magic_attack", 0),
        defence=data.get("defence", 0),
        magic_defence=data.get("magic_defence", 0),
        speed=data.get("speed", 0),
        resistance=data.get("resistance", 0),
    )


def _load_item(data: dict[str, Any]) -> Item:
    return Item(
        item_id=data["item_id"],
        name=data["name"],
        description=data.get("description", ""),
        item_type=enum_from_name(ItemType, data["item_type"]),
        rarity=enum_from_name(ItemRarity, data.get("rarity", "COMMON")),
        equip_slot=enum_from_name(EquipSlot, data.get("equip_slot", "NONE")),
        buy_price=data.get("buy_price", 0),
        sell_price=data.get("sell_price", 0),
        stackable=data.get("stackable", True),
        max_stack=data.get("max_stack", 99),
        stat_modifiers=_load_stat_modifiers(data.get("stat_modifiers", {})),
        restores_hp=data.get("restores_hp", 0),
        restores_mp=data.get("restores_mp", 0),
        cures_status=tuple(data.get("cures_status", [])),
        icon_key=data.get("icon_key"),
    )


def load_catalog_from_json(path: Path | str) -> ItemCatalog:
    catalog = ItemCatalog()
    for item in load_objects_from_json(path, _load_item):
        catalog.register(item)
    return catalog


def build_items_catalog() -> ItemCatalog:
    """Returns JSON data"""
    return load_catalog_from_json(Path(__file__).resolve().parent / "items.json")
