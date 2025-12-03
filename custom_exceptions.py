# Custom exceptions for Project 3

class InvalidCharacterClassError(Exception):
    pass

class CharacterNotFoundError(Exception):
    pass

class SaveFileCorruptedError(Exception):
    pass

class InvalidSaveDataError(Exception):
    pass

class CharacterDeadError(Exception):
    pass

class InventoryFullError(Exception):
    pass

class ItemNotFoundError(Exception):
    pass

class InsufficientResourcesError(Exception):
    pass

class InvalidItemTypeError(Exception):
    pass

class QuestNotFoundError(Exception):
    pass

class InsufficientLevelError(Exception):
    pass

class QuestRequirementsNotMetError(Exception):
    pass

class QuestAlreadyCompletedError(Exception):
    pass

class QuestNotActiveError(Exception):
    pass

class MissingDataFileError(Exception):
    pass

class InvalidDataFormatError(Exception):
    pass

class InvalidTargetError(Exception):
    pass

class CombatNotActiveError(Exception):
    pass
