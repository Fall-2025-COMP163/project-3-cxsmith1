# main.py
import os
import sys
from character_manager import create_character, save_character, load_character, Player
from inventory_system import Inventory
from quest_handler import QuestHandler
from combat_system import engage
from game_data import load_items, load_quests, get_enemy_template

SAVE_DIR = os.path.join(os.path.dirname(__file__), "data", "save_games")

def simple_menu():
    print("=== Quest Chronicles (simple launcher) ===")
    print("1) New character")
    print("2) Load character")
    print("3) Exit")
    choice = input("> ").strip()
    return choice

def choose_class():
    print("Choose a class exactly as written:")
    print("Warrior, Mage, Rogue, Cleric")
    cl = input("Class: ").strip()
    return cl

def run():
    while True:
        c = simple_menu()
        if c == "1":
            name = input("Name: ").strip()
            cl = choose_class()
            try:
                player = create_character(name, cl)
            except Exception as e:
                print("Failed to create character:", e)
                continue
            print(f"Created {player.name} the {player.character_class}")
        elif c == "2":
            files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
            if not files:
                print("No saves present.")
                continue
            print("Saves:")
            for i,f in enumerate(files,1):
                print(f"{i}) {f}")
            sel = input("Pick: ").strip()
            try:
                idx = int(sel)-1
                player = load_character(files[idx])
                print(f"Loaded {player.name} the {player.character_class}")
            except Exception as e:
                print("Load failed:", e)
                continue
        elif c == "3":
            print("Bye.")
            sys.exit(0)
        else:
            print("Invalid choice.")
            continue

        # small loop while player exists
        inv = Inventory()
        quests = QuestHandler()
        while True:
            print("\n--- Player Menu ---")
            print("1) Show stats")
            print("2) List quests")
            print("3) Take quest")
            print("4) Go on assigned quest (fight)")
            print("5) Save and exit to main menu")
            cmd = input("> ").strip()
            if cmd == "1":
                print(player.to_dict())
            elif cmd == "2":
                for q in quests.list_available():
                    print(f"{q.id}: {q.title} - {q.description} (xp:{q.xp}, gold:{q.gold})")
            elif cmd == "3":
                qid = input("Quest id: ").strip()
                try:
                    q = quests.assign(player, qid)
                    print(f"Assigned: {q.title}")
                except Exception as e:
                    print("Assign failed:", e)
            elif cmd == "4":
                assigned = quests.get_assigned(player)
                if not assigned:
                    print("No assigned quests.")
                    continue
                q = assigned[0]
                enemy = quests.spawn_enemy_for_quest(q)
                print(f"Fighting {enemy['name']} (HP {enemy['health']})")
                res = engage(player, enemy)
                for line in res["log"]:
                    print(line)
                if res["victory"]:
                    print("You won!")
                    print(f"Earned {res['xp']} xp and {res['gold']} gold.")
                    player.xp += res["xp"]
                    player.gold += res["gold"]
                    quests.complete(player, q.id)
                else:
                    print("You were defeated. You can save and exit to recover.")
            elif cmd == "5":
                fname = input("Save filename (end with .json): ").strip()
                try:
                    path = save_character(player, fname)
                    print("Saved to", path)
                except Exception as e:
                    print("Save failed:", e)
                break
            else:
                print("Unknown command.")

if __name__ == "__main__":
    run()
