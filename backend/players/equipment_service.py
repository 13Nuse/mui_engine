"""
backend/players/equipment_service.py

Bridges the party memeber and inventory so the item
being used always moves around between the two.
"""

from __future__ import annotations

from backend.inventory.models import Inventory
from backend.items.models import EquipmentItem, EquipSlot
from backend.players.models import PartyMember


def equip_from_inventory(
        member: PartyMember, 
        inventory: Inventory,
        item_id: str,
        ) -> bool:
    """
    Takes item_id from inventory and equips it on a member.
    If something is already equipped in the slot, it goes back
    into inventory.
    """
    item = inventory.registry.items.get(item_id)
    if item is None or not isinstance(item, EquipmentItem):
        return False
    if not inventory.remove_item(item_id, 1):
        return False

    previous_equip = member.equip(item)
    if previous_equip is not None:
        inventory.add_item(previous_equip.item_id, 1)
    return True

def unequip_to_inventory(
        member: PartyMember,
        inventory: Inventory,
        slot: EquipSlot,
        ) -> bool:
    """
    Removes equipment in slot and returns to inventory.
    """
    previous_equip = member.unequip(slot)
    if previous_equip is None:
        return False
    inventory.add_item(previous_equip.item_id, 1)
    return True


    
