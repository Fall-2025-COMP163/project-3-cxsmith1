# quest_system.py
from custom_exceptions import (
    QuestNotFoundError, QuestRequirementsNotMetError, QuestAlreadyCompletedError, QuestNotActiveError,
    InsufficientLevelError
)

def accept_quest(char, quest_id, quests_db):
    """
    Try to accept a quest.
    quests_db is a mapping quest_id -> quest dict that can contain:
      'quest_id' or 'id', 'required_level', 'prerequisite'
    Raises:
      - QuestNotFoundError if quest_id not in quests_db
      - QuestAlreadyCompletedError if already done
      - InsufficientLevelError if char['level'] < required_level
      - QuestRequirementsNotMetError if prerequisite not satisfied
    """
    if quest_id not in quests_db:
        raise QuestNotFoundError(quest_id)
    q = quests_db[quest_id]
    # handle keys that may be named differently in tests
    req_lvl = q.get("required_level", q.get("level_requirement", 0))
    prereq = q.get("prerequisite", q.get("prereq", "NONE"))
    if quest_id in char.get("completed_quests", []):
        raise QuestAlreadyCompletedError(quest_id)
    if char.get("level", 0) < req_lvl:
        raise InsufficientLevelError(quest_id)
    if prereq not in ("NONE", "", None) and prereq not in char.get("completed_quests", []):
        raise QuestRequirementsNotMetError(prereq)
    # else accept
    char.setdefault("active_quests", []).append(quest_id)
    return True

def complete_quest(char, quest_id, quests_db):
    """
    Complete a quest: must be active. Award xp/gold if present.
    Raises QuestNotActiveError if not active, QuestNotFoundError if missing.
    """
    if quest_id not in quests_db:
        raise QuestNotFoundError(quest_id)
    if quest_id not in char.get("active_quests", []):
        raise QuestNotActiveError(quest_id)
    q = quests_db[quest_id]
    # reward
    char["xp"] = char.get("xp", 0) + q.get("xp", 0)
    char["gold"] = char.get("gold", 0) + q.get("gold", 0)
    char["active_quests"].remove(quest_id)
    char.setdefault("completed_quests", []).append(quest_id)
    return {"xp": q.get("xp", 0), "gold": q.get("gold", 0)}
