import os
from custom_exceptions import DataError

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def _read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    except Exception as e:
        raise DataError(f"Failed to load {path}: {e}")

def load_items():
    lines = _read_lines(os.path.join(DATA_DIR, "items.txt"))
    items = {}
    for i, line in enumerate(lines, start=1):
        parts = line.strip().split(",")
        if len(parts) != 3:
            raise DataError(f"Malformed items.txt line {i}: {line}")
        item_id, name, value_str = parts
        try:
            value = int(value_str)
        except ValueError:
            raise DataError(f"Invalid value for item {item_id} on line {i}")
        items[item_id] = {"name": name, "value": value}
    return items

def load_quests():
    lines = _read_lines(os.path.join(DATA_DIR, "quests.txt"))
    quests = {}
    for i, line in enumerate(lines, start=1):
        parts = line.strip().split(",")
        if len(parts) != 5:  # Expect 5 fields now
            raise DataError(f"Malformed quests.txt line {i}: {line}")
        quest_id, title, description, xp_str, gold_str = parts
        try:
            xp = int(xp_str)
            gold = int(gold_str)
        except ValueError:
            raise DataError(f"Invalid XP or gold for quest {quest_id} on line {i}")
        quests[quest_id] = {
            "id": quest_id,
            "title": title,
            "description": description,
            "xp": xp,
            "gold": gold
        }
    return quests

def enemy_templates():
    return {
        "goblin": {"name": "goblin", "health": 30, "strength": 6, "magic": 0, "xp": 10, "gold": 5},
        "orc":    {"name": "orc",    "health": 60, "strength": 12, "magic": 0, "xp": 25, "gold": 15},
        "dragon": {"name": "dragon", "health": 200,"strength": 25, "magic": 15, "xp": 200,"gold": 150}
    }

def get_enemy_template(name):
    return enemy_templates().get(name.lower())
