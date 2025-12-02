# quest_handler.py
from game_data import load_quests, get_enemy_template
from custom_exceptions import QuestError
import random

class Quest:
    def __init__(self, qdict):
        self.id = qdict["id"]
        self.title = qdict["title"]
        self.description = qdict["description"]
        self.xp = qdict["xp"]
        self.gold = qdict["gold"]
        self.enemy = qdict.get("enemy")

class QuestHandler:
    def __init__(self, quests_db=None):
        self.quests = {}
        if quests_db is None:
            raw = load_quests()
        else:
            raw = quests_db
        for qid, q in raw.items():
            self.quests[qid] = Quest(q)
        self.assigned = {}  # player_name -> list of quest ids

    def list_available(self):
        return list(self.quests.values())

    def assign(self, player, quest_id):
        if quest_id not in self.quests:
            raise QuestError("Quest not found.")
        self.assigned.setdefault(player.name, []).append(quest_id)
        return self.quests[quest_id]

    def get_assigned(self, player):
        return [self.quests[qid] for qid in self.assigned.get(player.name, [])]

    def complete(self, player, quest_id):
        if quest_id not in self.assigned.get(player.name, []):
            raise QuestError("Quest not assigned to player.")
        q = self.quests[quest_id]
        # reward player
        player.xp += q.xp
        player.gold += q.gold
        self.assigned[player.name].remove(quest_id)
        return {"xp": q.xp, "gold": q.gold}

    def spawn_enemy_for_quest(self, quest):
        if not quest.enemy:
            # random simple enemy pick
            names = ["goblin", "orc"]
            return get_enemy_template(random.choice(names)).copy()
        tmpl = get_enemy_template(quest.enemy)
        if tmpl is None:
            raise QuestError("Unknown enemy for quest.")
        return tmpl.copy()
