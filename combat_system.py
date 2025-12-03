from custom_exceptions import InvalidTargetError, CombatNotActiveError

class SimpleBattle:
    def __init__(self, player, enemy):
        if not isinstance(player, dict) or not isinstance(enemy, dict):
            raise InvalidTargetError()
        self.player = player
        self.enemy = enemy
        self.combat_active = True

    def attack(self, attacker, defender, damage):
        if not self.combat_active:
            raise CombatNotActiveError()
        defender["health"] -= damage
        if defender["health"] < 0:
            defender["health"] = 0
