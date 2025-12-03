from custom_exceptions import QuestNotFoundError, InsufficientLevelError, QuestRequirementsNotMetError, QuestAlreadyCompletedError, QuestNotActiveError

def start_quest(character, quest_id, quests):
    if quest_id not in quests:
        raise QuestNotFoundError()
    quest = quests[quest_id]
    if character["level"] < quest.get("required_level",1):
        raise InsufficientLevelError()
    prereq = quest.get("prerequisite")
    if prereq and prereq not in character["completed_quests"]:
        raise QuestRequirementsNotMetError()
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError()
    character["active_quests"].append(quest_id)

def complete_quest(character, quest_id, quests):
    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError()
    character["active_quests"].remove(quest_id)
    character["completed_quests"].append(quest_id)
