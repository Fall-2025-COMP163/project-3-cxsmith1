# inventory_system.py

from custom_exceptions import InventoryError, InventoryFullError

# ---------------------------
# Inventory Management
# ---------------------------

MAX_INVENTORY_SIZE = 20  # maximum items a character can carry


def add_item_to_inventory(character, item):
    """Add an item to the character's inventory."""
    if len(character.inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"{character.name}'s inventory is full.")
    character.inventory.append(item)
    return True


def remove_item_from_inventory(character, item):
    """Remove an item from the inventory."""
    if item not in character.inventory:
        raise InventoryError(f"{item} not found in inventory.")
    character.inventory.remove(item)
    return True


def use_item(character, item):
    """Use an item from inventory. For now, just remove it."""
    if item not in character.inventory:
        raise InventoryError(f"{item} not in inventory.")
    character.inventory.remove(item)
    # Later, could add effects like healing, buffs, etc.
    return True


def equip_weapon(character, weapon):
    """Equip a weapon. Just add to inventory for now if not present."""
    if weapon not in character.inventory:
        character.inventory.append(weapon)
    character.equipped_weapon = weapon
    return True


def equip_armor(character, armor):
    """Equip armor. Just add to inventory if not present."""
    if armor not in character.inventory:
        character.inventory.append(armor)
    character.equipped_armor = armor
    return True


def purchase_item(character, item, cost):
    """Purchase an item. Deduct gold and add to inventory."""
    if character.gold < cost:
        raise InventoryError(f"Not enough gold to buy {item}.")
    from character_manager import add_gold

    add_gold(character, -cost)
    add_item_to_inventory(character, item)
    return True


def sell_item(character, item, price):
    """Sell an item. Remove from inventory and add gold."""
    if item not in character.inventory:
        raise InventoryError(f"{item} not in inventory.")
    from character_manager import add_gold

    remove_item_from_inventory(character, item)
    add_gold(character, price)
    return True
