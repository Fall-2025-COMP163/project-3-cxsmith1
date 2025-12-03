from custom_exceptions import InventoryFullError, ItemNotFoundError, InsufficientResourcesError, InvalidItemTypeError

MAX_INVENTORY_SIZE = 10

def add_item(character, item):
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError()
    character["inventory"].append(item)

def remove_item(character, item):
    if item not in character["inventory"]:
        raise ItemNotFoundError()
    character["inventory"].remove(item)

def use_item(character, item):
    if item not in character["inventory"]:
        raise ItemNotFoundError()
    # For simplicity, only allow healing potions
    if item.startswith("potion"):
        character["health"] += 20
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]
        character["inventory"].remove(item)
    else:
        raise InvalidItemTypeError()
