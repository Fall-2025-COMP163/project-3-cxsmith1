# custom_exceptions.py
# Minimal set of exceptions expected by the tests

class GameError(Exception):
    pass

# Data
class DataError(GameError):
    pass

class MissingDataFileError(DataError):
    pass

class InvalidDataFormatError(DataError):
    pass

# Character
class CharacterError(GameError):
    pass

class InvalidCharacterClassError(CharacterError):
    pass

class CharacterNotFoundError(CharacterError):
    pass

class CharacterDeadError(CharacterError):
    pass

class InsufficientLevelError(CharacterError):
    pass

# Inventory
class InventoryError(GameError):
    pass

class InventoryFullError(InventoryError):
    pass

class ItemNotFoundError(InventoryError):
    pass

class InsufficientResourcesError(InventoryError):
    pass

class InvalidItemTypeError(InventoryError):
    pass

# Quest
class QuestError(GameError):
    pass

class QuestNotFoundError(QuestError):
    pass

class QuestRequirementsNotMetError(QuestError):
    pass

class QuestAlreadyCompletedError(QuestError):
    pass

class QuestNotActiveError(QuestError):
    pass

# Combat
class CombatError(GameError):
    pass

class InvalidTargetError(CombatError):
    pass

class CombatNotActiveError(CombatError):
    pass
