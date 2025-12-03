# character_manager.py

import os
from custom_exceptions import (
    InvalidDataFormatError,
    CharacterNotFoundError,
    CharacterError
)

# ---------------------------
# Player class
# ---------------------------
class Player:
    def __init__(self, name, character_class):
        valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
        if character_class not in valid_classes:
            raise CharacterError(f"Invalid character class: {character_class}")

        self.name = name
        self.character_class = character_class
        self.level = 1
        self.experience = 0
        self.gold = 100
        self.inventory = []
        self.active_quests = []
        self.completed_quests = []

        if character_class == "Warrior":
            self.health = self.max_health = 120
            self.strength = 15
            self.magic = 5
        elif character_class == "Mage":
            self.health = self.max_health = 80
            self.strength = 8
            self.magic = 20
        elif character_class == "Rogue":
            self.health = self.max_health = 90
            self.strength = 12
            self.magic = 10
        elif character_class == "Cleric":
            self.health = self.max_health = 100
            self.strength = 10
            self.magic = 15


# ---------------------------
# Character functions
# ---------------------------
def create_character(name, character_class):
    return Player(name, character_class)


def save_character(character, save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    filename = os.path.join(save_directory, f"{character.name}_save.txt")
    try:
        with open(filename, "w") as f:
            f.write(f"NAME:{character.name}\n")
            f.write(f"CLASS:{character.character_class}\n")
            f.write(f"LEVEL:{character.level}\n")
            f.write(f"HEALTH:{character.health}\n")
            f.write(f"MAX_HEALTH:{character.max_health}\n")
            f.write(f"STRENGTH:{character.strength}\n")
            f.write(f"MAGIC:{character.magic}\n")
            f.write(f"EXPERIENCE:{character.experience}\n")
            f.write(f"GOLD:{character.gold}\n")
            f.write(f"INVENTORY:{','.join(character.inventory)}\n")
            f.write(f"ACTIVE_QUESTS:{','.join(character.active_quests)}\n")
            f.write(f"COMPLETED_QUESTS:{','.join(character.completed_quests)}\n")
        return True
    except Exception as e:
        raise e


def load_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Save file for {character_name} not found.")
    try:
        with open(filename, "r") as f:
            data = {}
            for line in f:
                if ":" not in line:
                    continue
                key, value = line.strip().split(":", 1)
                data[key] = value

        # Convert to proper types
        player = Player(data["NAME"], data["CLASS"])
        player.level = int(data["LEVEL"])
        player.health = int(data["HEALTH"])
        player.max_health = int(data["MAX_HEALTH"])
        player.strength = int(data["STRENGTH"])
        player.magic = int(data["MAGIC"])
        player.experience = int(data["EXPERIENCE"])
        player.gold = int(data["GOLD"])
        player.inventory = data["INVENTORY"].split(",") if data["INVENTORY"] else []
        player.active_quests = data["ACTIVE_QUESTS"].split(",") if data["ACTIVE_QUESTS"] else []
        player.completed_quests = data["COMPLETED_QUESTS"].split(",") if data["COMPLETED_QUESTS"] else []

        return player
    except Exception as e:
        raise InvalidDataFormatError(f"Failed to load {character_name}: {e}")


def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []
    return [
        f.replace("_save.txt", "")
        for f in os.listdir(save_directory)
        if f.endswith("_save.txt")
    ]


def delete_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"{character_name} does not exist.")
    os.remove(filename)
    return True


# ---------------------------
# Character operations
# ---------------------------
def gain_experience(character, xp_amount):
    if character.health <= 0:
        raise CharacterError("Cannot gain XP: character is dead.")
    character.experience += xp_amount
    while character.experience >= character.level * 100:
        character.experience -= character.level * 100
        character.level += 1
        character.max_health += 10
        character.strength += 2
        character.magic += 2
        character.health = character.max_health


def add_gold(character, amount):
    if character.gold + amount < 0:
        raise ValueError("Not enough gold.")
    character.gold += amount
    return character.gold


def heal_character(character, amount):
    if character.health <= 0:
        return 0
    healed = min(amount, character.max_health - character.health)
    character.health += healed
    return healed


def is_character_dead(character):
    return character.health <= 0


def revive_character(character):
    if character.health > 0:
        return False
    character.health = character.max_health // 2
    return True


def validate_character_data(character):
    required_fields = [
        "name", "character_class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]
    for field in required_fields:
        if not hasattr(character, field):
            raise InvalidDataFormatError(f"Missing field: {field}")
    return True
