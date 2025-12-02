# inventory_system.py
from custom_exceptions import ItemNotFoundError
import os
from game_data import load_items

class Inventory:
    def __init__(self, items_db=None):
        # items_db: mapping item_id -> item dict (loaded from game_data)
        self._items_db = items_db if items_db is not None else load_items()
        self.items = []  # list of item ids

    def add(self, item_id):
        if item_id not in self._items_db:
            raise ItemNotFoundError(f"Item '{item_id}' not found.")
        self.items.append(item_id)

    def remove(self, item_id):
        try:
            self.items.remove(item_id)
        except ValueError:
            raise ItemNotFoundError(f"Item '{item_id}' not in inventory.")

    def list(self):
        return [self._items_db[i] for i in self.items]

    def get_item(self, item_id):
        if item_id not in self._items_db:
            raise ItemNotFoundError(f"Item '{item_id}' not found.")
        return self._items_db[item_id]

    def equip(self, item_id, player):
        item = self.get_item(item_id)
        typ = item.get("type","").lower()
        if typ == "weapon":
            player.equipped["weapon"] = item
        elif typ == "armor":
            player.equipped["armor"] = item
        else:
            # consumable -- using equip acts like use
            return self.use(item_id, player)
        return item

    def use(self, item_id, player):
        item = self.get_item(item_id)
        if item["type"].lower() == "consumable":
            # simple effect parsing: effect like heal:20 or str:+5
            eff = item.get("effect","")
            if eff.startswith("heal:"):
                amount = int(eff.split(":",1)[1])
                player.health = min(player.max_health, player.health + amount)
                try:
                    self.remove(item_id)
                except ItemNotFoundError:
                    pass
                return {"used":True, "effect":"heal", "amount":amount}
        # other effects ignored for simplicity
        return {"used":False}
