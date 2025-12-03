# combat_system.py
import random
from custom_exceptions import InvalidTargetError, CombatNotActiveError

def create_enemy(template):
    """
    template: dict with 'name' and 'health' keys OR a string name handled simply.
    Returns an enemy dict or raises InvalidTargetError if template invalid.
    """
    if isinstance(template, dict):
        if "name" not in template or "health" not in template:
            raise InvalidTargetError("Invalid enemy template")
        return dict(template)  # shallow copy
    if isinstance(template, str):
        # small builtin templates
        name = template.lower()
        if name == "goblin":
            return {"name": "goblin", "health": 30, "strength": 6, "xp": 10, "gold": 5}
        if name == "orc":
            return {"name": "orc", "health": 60, "strength": 12, "xp": 25, "gold": 15}
        raise InvalidTargetError("Unknown enemy")
    raise InvalidTargetError("Invalid enemy")

class SimpleBattle:
    def __init__(self, player, enemy):
        # expect player and enemy to be dict-like
        self.player = player
        self.enemy = enemy
        self.combat_active = True

    def attack(self):
        """
        One step of attack: player hits enemy then enemy hits player.
        Raises CombatNotActiveError if combat_active is False.
        """
        if not self.combat_active:
            raise CombatNotActiveError("Combat not active")
        # player attack: use player['strength'] if dict-like, else attribute
        atk = self.player.get("strength", 0) if isinstance(self.player, dict) else getattr(self.player, "strength", 0)
        # small crit
        if random.random() < 0.1:
            atk = int(atk * 1.5)
        self.enemy["health"] = max(0, self.enemy.get("health", 0) - atk)
        # enemy retaliates if alive
        if self.enemy.get("health", 0) > 0:
            edmg = self.enemy.get("strength", 0)
            if random.random() < 0.05:
                edmg = int(edmg * 1.5)
            self.player["health"] = max(0, self.player.get("health", 0) - edmg)
        # return snapshot
        return {
            "player_hp": self.player.get("health", 0),
            "enemy_hp": self.enemy.get("health", 0)
        }
