# combat_system.py
import random
from custom_exceptions import GameError

def basic_attack(attacker, defender):
    """Attacker and defender can be Player-like or enemy dicts.
    Use strength for physical, magic for magical where appropriate.
    """
    dmg = getattr(attacker, "strength", None)
    if dmg is None:
        dmg = attacker.get("strength", 0)
    # small crit chance
    if random.random() < 0.1:
        dmg = int(dmg * 1.5)
    defender["health"] -= dmg
    if defender["health"] < 0:
        defender["health"] = 0
    return dmg

def engage(player, enemy):
    """Return result dict. enemy is a dict with health/strength/magic keys."""
    if not isinstance(enemy, dict):
        raise GameError("Enemy must be a dict.")
    log = []
    # simple turn-based: player always goes first
    while player.health > 0 and enemy["health"] > 0:
        # player attacks
        dmg = basic_attack(player, enemy)
        log.append(f"{player.name} deals {dmg} to {enemy['name']}. ({enemy['health']} HP left)")
        if enemy["health"] <= 0:
            break
        # enemy attacks (use enemy strength)
        edmg = enemy.get("strength", 0)
        # enemy crit small chance
        if random.random() < 0.05:
            edmg = int(edmg * 1.5)
        player.health -= edmg
        if player.health < 0:
            player.health = 0
        log.append(f"{enemy['name']} deals {edmg} to {player.name}. ({player.health} HP left)")
    victory = enemy["health"] <= 0 and player.health > 0
    return {
        "victory": victory,
        "player_hp": player.health,
        "enemy_hp": enemy["health"],
        "log": log,
        "xp": enemy.get("xp", 0) if victory else 0,
        "gold": enemy.get("gold", 0) if victory else 0
    }
