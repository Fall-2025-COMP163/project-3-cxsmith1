# character_manager.py
import os
import json
from custom_exceptions import InvalidTargetError

SAVE_DIR = os.path.join(os.path.dirname(__file__), "data", "save_games")
os.makedirs(SAVE_DIR, exist_ok=True)

class Player:
    def __init__(self, name, character_class, level=1, hp=None, strength=None, magic=None, gold=0, xp=0):
        self.name = name
        self.character_class = character_class  # "Warrior","Mage","Rogue","Cleric"
        self.level = int(level)
        # default stats for classes
        base = {
            "Warrior": {"health": 120, "strength": 15, "magic": 5},
            "Mage":    {"health": 80,  "strength": 8,  "magic": 20},
            "Rogue":   {"health": 90,  "strength": 12, "magic": 10},
            "Cleric":  {"health": 100, "strength": 9,  "magic": 14}
        }
        if character_class not in base:
            raise InvalidClassError(f"Class must be one of {list(base.keys())}")
        defaults = base[character_class]
        self.max_health = hp if hp is not None else defaults["health"]
        self.health = self.max_health
        self.strength = strength if strength is not None else defaults["strength"]
        self.magic = magic if magic is not None else defaults["magic"]
        self.gold = gold
        self.xp = xp
        self.inventory = []  # list of item ids or dicts
        self.equipped = {"weapon": None, "armor": None}
    def to_dict(self):
        return {
            "name": self.name,
            "class": self.character_class,
            "level": self.level,
            "health": self.health,
            "max_health": self.max_health,
            "strength": self.strength,
            "magic": self.magic,
            "gold": self.gold,
            "xp": self.xp,
            "inventory": self.inventory,
            "equipped": self.equipped
        }
    @classmethod
    def from_dict(cls, d):
        p = cls(d["name"], d["class"], d.get("level",1),
                d.get("max_health"), d.get("strength"), d.get("magic"),
                gold=d.get("gold",0), xp=d.get("xp",0))
        p.health = d.get("health", p.max_health)
        p.inventory = d.get("inventory", [])
        p.equipped = d.get("equipped", {"weapon":None,"armor":None})
        return p

def create_character(name, class_name):
    """Factory to create a Player. class_name must be exact: 'Warrior','Mage','Rogue','Cleric'"""
    return Player(name, class_name)

def save_character(player, filename):
    path = os.path.join(SAVE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(player.to_dict(), f, indent=2)
    return path

def load_character(filename):
    path = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"No save file at {path}")
    import json
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Player.from_dict(data)
