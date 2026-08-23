"""
backend/inventory/models.py

Models the inventory a player or a shop, via composition carries.
Slots hold an item_id plus quantity rather than full Item objects, so the
inventory stays cheap to serialize to the frontend, the frontend system
resolves item_id(Item) via ItemCatalog.

"""

from __future__ import annotation

from dataclasses import dataclass, field
from typing import Optional

from backend.items.models import Item
from backend.items.item_catalog import ItemCatalog
from core.settings import ItemType, PlayerConfig



@dataclass(slots=True)
class InventorySlot:
    item_id: str
    quantity: int = 1

    def is_empty(self) -> bool:
        return self.quantity <= 0


@dataclass
class Inventory:
    gold: int = 0
    max_slots: int = PlayerConfig.MAX_INVENTORY_SIZE
    catalog: ItemCatalog = field(default_factory=ItemCatalog)
    slots: list[Optional[InventorySlot]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.slots:
            self.slots = [None] * self.max_slots
        elif len(self.slots) != self.max_slots:
            raise ValueError("slots length must match max_slots")

    # queries
    def find_slot_index(self, item_id: str) -> Optional[int]:
        for item, slot in enumerate(self.slots):
            if slot is not None and slot.item_id == item_id:
                return item
        return None

    def first_empty_index(self) -> Optional[int]:
        for item, slot in enumerate(self.slots):
            if slot is None:
                return item
        return None

    def quantity_of(self, item_id: str) -> int:
        return sum(slot.quantity for slot in self.slots if slot is not None and slot.item_id == item_id)

    def is_full(self) -> bool:
        return self.first_empty_index() is None

    # mutations
    def add_item(self, item_id: str, quantity: int = 1) -> int:
        """Adds up to `quantity` of an item, stacking where possible.
        Returns how many units could NOT be added (0 = fully added)."""
        item: Item = self.catalog.get(item_id)
        remaining = quantity
        max_stack = item.max_stack if item.stackable else 1

        if item.stackable:
            existing_index = self.find_slot_index(item_id)
            while existing_index is not None and remaining > 0:
                slot = self.slots[existing_index]
                space = max_stack - slot.quantity
                if space > 0:
                    added = min(space, remaining)
                    slot.quantity += added
                    remaining -= added
                if remaining <= 0:
                    return 0
                existing_index = self._find_slot_with_space(item_id, max_stack)

        while remaining > 0:
            empty_index = self.first_empty_index()
            if empty_index is None:
                break
            take = min(max_stack, remaining)
            self.slots[empty_index] = InventorySlot(item_id=item_id, quantity=take)
            remaining -= take

        return remaining

    def _find_slot_with_space(self, item_id: str, max_stack: int) -> Optional[int]:
        for i, slot in enumerate(self.slots):
            if slot is not None and slot.item_id == item_id and slot.quantity < max_stack:
                return i
        return None

    def remove_item(self, item_id: str, quantity: int = 1) -> int:
        """Removes up to `quantity` of an item. Returns how many units
        were actually removed."""
        removed = 0
        for i, slot in enumerate(self.slots):
            if remaining_to_remove := (quantity - removed):
                if slot is not None and slot.item_id == item_id:
                    take = min(slot.quantity, remaining_to_remove)
                    slot.quantity -= take
                    removed += take
                    if slot.is_empty():
                        self.slots[i] = None
            else:
                break
        return removed

    def has_item(self, item_id: str, quantity: int = 1) -> bool:
        return self.quantity_of(item_id) >= quantity

    def get_quantity(self, item_id: str) -> int:
        return self.quantity_of(item_id)

    def list_slots(self, category: ItemType | None = None) -> list[InventorySlot]:
        slots = []
        for item_id, quantity in self.quantity_of.items():
            item = self.registry.get(item_id)
            if category is not None and item.category !=  category:
                continue
            slots.append(InventorySlot(item=item, quantity=quantity))
        slots.sort(key=lambda entry: entry.item.name)
        return slots

    # gold
    def add_gold(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("use spend_gold for negative amounts")
        self.gold += amount

    def spend_gold(self, amount: int) -> bool:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if self.gold < amount:
            return False
        self.gold -= amount
        return True

    def to_view_dict(self) -> dict:
        """Serialize into a plain dict the frontend can consume to draw
        the inventory grid without needing backend classes directly."""
        return {
            "gold": self.gold,
            "slots": [
                None if s is None else {
                    "item_id": s.item_id,
                    "quantity": s.quantity,
                    "name": self.catalog.get(s.item_id).name,
                    "icon_key": self.catalog.get(s.item_id).icon_key,
                }
                for s in self.slots
            ],
        }

# Inventory testing
def build_starting_inventory(registry: ItemCatalog) -> Inventory:
    inventory = Inventory(registry=registry, gold=1000)
    inventory.add_item("potions", 5)
    return inventory
