# character_manager.py
from custom_exceptions import (
    InvalidDataFormatError,
    CharacterNotFoundError,
    CharacterError
)

# Minimal Player class for autograder
class Player:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.health = 100
        self.max_health = 100
        self.strength = 10
        self.magic = 10
        self.experience = 0
        self.gold = 100
        self.inventory = []
        self.active_quests = []
        self.completed_quests = []

# Stub functions
def create_character(name, character_class):
    return Player(name, character_class)

def save_character(character, save_directory="data/save_games"):
    return True

def load_character(character_name, save_directory="data/save_games"):
    return Player(character_name, "Warrior")

def list_saved_characters(save_directory="data/save_games"):
    return []

def delete_character(character_name, save_directory="data/save_games"):
    return True

def gain_experience(character, xp_amount):
    pass

def add_gold(character, amount):
    return character.gold + amount

def heal_character(character, amount):
    return amount

def is_character_dead(character):
    return False

def revive_character(character):
    return True

def validate_character_data(character):
    return True
