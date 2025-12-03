import os
from custom_exceptions import *

def create_character(name, character_class):
    base = {
        "Warrior": {"health":120, "strength":15, "magic":5},
        "Mage": {"health":80, "strength":8, "magic":20},
        "Rogue": {"health":90, "strength":12, "magic":10},
        "Cleric": {"health":100, "strength":9, "magic":14}
    }
    if character_class not in base:
        raise InvalidCharacterClassError(f"Class must be one of {list(base.keys())}")

    stats = base[character_class]
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": stats["health"],
        "max_health": stats["health"],
        "strength": stats["strength"],
        "magic": stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }
    return character

SAVE_DIR = "data/save_games"

def save_character(character, save_directory=SAVE_DIR):
    os.makedirs(save_directory, exist_ok=True)
    filename = os.path.join(save_directory, f"{character['name']}_save.txt")
    try:
        with open(filename, "w") as f:
            for key in ["name","class","level","health","max_health","strength","magic","experience","gold"]:
                f.write(f"{key.upper()}: {character[key]}\n")
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")
        return True
    except Exception as e:
        raise e

def load_character(character_name, save_directory=SAVE_DIR):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file at {filename}")
    try:
        character = {}
        with open(filename) as f:
            for line in f:
                if ":" not in line:
                    raise InvalidSaveDataError()
                key, val = line.strip().split(":",1)
                key = key.lower()
                val = val.strip()
                if key in ["level","health","max_health","strength","magic","experience","gold"]:
                    character[key] = int(val)
                elif key in ["inventory","active_quests","completed_quests"]:
                    character[key] = val.split(",") if val else []
                else:
                    character[key] = val
        return character
    except InvalidSaveDataError:
        raise
    except Exception:
        raise SaveFileCorruptedError()

def list_saved_characters(save_directory=SAVE_DIR):
    if not os.path.exists(save_directory):
        return []
    files = os.listdir(save_directory)
    return [f.replace("_save.txt","") for f in files if f.endswith("_save.txt")]

def delete_character(character_name, save_directory=SAVE_DIR):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError()
    os.remove(filename)
    return True

def gain_experience(character, xp_amount):
    if character["health"] <= 0:
        raise CharacterDeadError()
    character["experience"] += xp_amount
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]

def add_gold(character, amount):
    if character["gold"] + amount < 0:
        raise ValueError()
    character["gold"] += amount
    return character["gold"]

def heal_character(character, amount):
    healed = min(amount, character["max_health"] - character["health"])
    character["health"] += healed
    return healed

def is_character_dead(character):
    return character["health"] <= 0

def revive_character(character):
    character["health"] = character["max_health"] // 2
    return True

def validate_character_data(character):
    required = ["name","class","level","health","max_health","strength","magic",
                "experience","gold","inventory","active_quests","completed_quests"]
    for key in required:
        if key not in character:
            raise InvalidSaveDataError()
    for key in ["level","health","max_health","strength","magic","experience","gold"]:
        if not isinstance(character[key], int):
            raise InvalidSaveDataError()
    for key in ["inventory","active_quests","completed_quests"]:
        if not isinstance(character[key], list):
            raise InvalidSaveDataError()
    return True
