# inventory_system.py
from custom_exceptions import (
    ItemNotFoundError, InventoryFullError, InsufficientResourcesError, InvalidItemTypeError
)

# tests reference this constant
MAX_INVENTORY_SIZE = 20

def add_item(char, item_id, items_db=None):
    """
    Add an item id to char['inventory'].
    - items_db can be a dict of available item ids (optional).
    - Raises InventoryFullError if char inventory is already maxed.
    - Raises ItemNotFoundError if an items_db is given and item_id not in it.
    """
    inv = char.setdefault("inventory", [])
    if len(inv) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full")
    if items_db is not None and item_id not in items_db:
        raise ItemNotFoundError(f"Item {item_id} not found")
    inv.append(item_id)
    return True

def remove_item(char, item_id):
    inv = char.get("inventory", [])
    if item_id not in inv:
        raise ItemNotFoundError(f"{item_id} not in inventory")
    inv.remove(item_id)
    return True

def purchase_item(char, item_data):
    """
    item_data is expected to be a dict with a 'cost' key.
    Raises InsufficientResourcesError if char['gold'] < cost.
    """
    cost = item_data.get("cost", 0)
    if char.get("gold", 0) < cost:
        raise InsufficientResourcesError("Not enough gold")
    char["gold"] -= cost
    return True

def use_item(char, item_id, item_data=None):
    """
    Use an item. If item_data provided and its type is non-consumable
    (e.g. 'weapon'), raise InvalidItemTypeError. If consumable heal, apply.
    item_data expected keys: 'type', 'effect' or 'value' optionally.
    """
    inv = char.get("inventory", [])
    if item_id not in inv:
        raise ItemNotFoundError(item_id)
    if item_data is not None:
        typ = item_data.get("type", "consumable").lower()
        if typ != "consumable":
            raise InvalidItemTypeError("Item type invalid for use")
        # consumable behavior: if effect 'heal:20' or value provided
        eff = item_data.get("effect")
        if isinstance(eff, str) and eff.startswith("heal:"):
            try:
                amt = int(eff.split(":", 1)[1])
            except:
                amt = 0
            char["health"] = min(char.get("max_health", char.get("health", 0)), char.get("health", 0) + amt)
            inv.remove(item_id)
            return {"used": True, "effect": "heal", "amount": amt}
        val = item_data.get("value")
        if isinstance(val, int):
            # treat as heal for simplicity
            char["health"] = min(char.get("max_health", char.get("health", 0)), char.get("health", 0) + val)
            inv.remove(item_id)
            return {"used": True, "amount": val}
    # default: mark not used
    return {"used": False}
