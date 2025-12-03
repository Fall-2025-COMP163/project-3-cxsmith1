# character_manager.py
import os
import json
from custom_exceptions import (
    InvalidCharacterClassError, CharacterNotFoundError, CharacterDeadError
)

SAVE_DIR = os.path.join(os.path.dirname(__file__), "data", "save_games")
os.makedirs(SAVE_DIR, exist_ok=True)

# base stats used to create characters
_CLASS_BASE = {
    "Warrior": {"health": 120, "strength": 15, "magic": 5},
    "Mage":    {"health": 80,  "strength": 8,  "magic": 20},
    "Rogue":   {"health": 90,  "strength": 12, "magic": 10},
    "Cleric":  {"health": 100, "strength": 9,  "magic": 14}
}

def create_character(name, character_class):
    """
    Return a character as a plain dict. Raises InvalidCharacterClassError
    if the class name is not one of the allowed keys.
    """
    if character_class not in _CLASS_BASE:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    base = _CLASS_BASE[character_class]
    char = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "gold": 0,
        "xp": 0,
        "inventory": [],
        "equipped": {"weapon": None, "armor": None},
        "active_quests": [],
        "completed_quests": []
    }
    return char

def save_character(char, filename):
    """Save the character dict to data/save_games/filename"""
    path = os.path.join(SAVE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(char, f, indent=2)
    return path

def load_character(filename):
    """Load character from data/save_games/filename. Raises CharacterNotFoundError if missing."""
    path = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(path):
        raise CharacterNotFoundError(f"No save file at {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def ensure_alive(char):
    """Helper used by tests: raises CharacterDeadError if health <= 0"""
    if char.get("health", 0) <= 0:
        raise CharacterDeadError("Character is dead")
    return True
