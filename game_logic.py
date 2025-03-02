import time
import random
import os

# Game state
class GameState:
    def __init__(self):
        self.player = {
            "name": "",
            "health": 100,
            "max_health": 100,
            "inventory": [],
            "equipped_weapon": None,
            "equipped_armor": None
        }
        self.current_location = "village"
        self.visited_locations = set()
        self.quest_progress = {
            "main_quest": 0,
            "forest_cleared": False,
            "mines_cleared": False,
            "castle_key": False
        }
        self.game_time = 0  # in minutes (in-game time)
        self.enemies_defeated = 0

# Items in the game
class Item:
    def __init__(self, name, description, item_type, value):
        self.name = name
        self.description = description
        self.item_type = item_type  # weapon, armor, potion, key_item
        self.value = value  # damage for weapons, defense for armor, healing for potions

# Define game items
def create_game_items():
    items = {
        "rusty_sword": Item("Rusty Sword", "An old sword with a dull edge.", "weapon", 5),
        "iron_sword": Item("Iron Sword", "A sturdy iron sword.", "weapon", 10),
        "enchanted_blade": Item("Enchanted Blade", "A magical sword that glows faintly blue.", "weapon", 20),
        
        "leather_armor": Item("Leather Armor", "Basic protection made of hardened leather.", "armor", 5),
        "chainmail": Item("Chainmail", "Interlocking metal rings provide solid protection.", "armor", 10),
        "knight_armor": Item("Knight's Armor", "Shining plate armor of exceptional quality.", "armor", 15),
        
        "health_potion": Item("Health Potion", "A red liquid that restores 25 health points.", "potion", 25),
        "greater_health_potion": Item("Greater Health Potion", "A crimson liquid that restores 50 health points.", "potion", 50),
        
        "village_map": Item("Village Map", "A crude map showing the surrounding areas.", "key_item", 0),
        "mine_key": Item("Mine Key", "An old iron key that opens the abandoned mines.", "key_item", 0),
        "castle_key": Item("Castle Key", "An ornate key with the royal crest.", "key_item", 0),
        "ancient_amulet": Item("Ancient Amulet", "A mysterious artifact with strange markings.", "key_item", 0)
    }
    return items

# Create enemies
class Enemy:
    def __init__(self, name, description, health, damage, loot=None):
        self.name = name
        self.description = description
        self.health = health
        self.damage = damage
        self.loot = loot if loot else []

# Define locations in the game
def create_game_world():
    world = {
        "village": {
            "name": "Village of Oakvale",
            "description": "A peaceful village with thatched-roof cottages and friendly people.",
            "connections": ["forest_path", "village_inn", "blacksmith", "village_square"],
            "enemies": [],
            "npcs": ["village_elder", "farmer", "merchant"],
            "items": ["village_map"]
        },
        # ... (rest of the locations)
    }
    return world

# Create NPCs
class NPC:
    def __init__(self, name, description, dialogue, trades=None, quest=None):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.trades = trades if trades else []
        self.quest = quest

# Define NPCs
def create_game_npcs():
    npcs = {
        "village_elder": NPC(
            "Elder Thorne", 
            "An elderly man with a long white beard and kind eyes.",
            {
                "greeting": "Welcome to Oakvale, traveler. Our village has faced troubled times lately.",
                "quest": "The forest has become dangerous, and our miners have gone missing. Would you help us?",
                "quest_active": "Have you checked the forest and the abandoned mines yet?",
                "quest_complete": "You've done a great service to our village. Take this as a token of our gratitude."
            },
            quest={
                "name": "Village Troubles",
                "description": "Investigate the forest and abandoned mines to discover what's causing problems for the village.",
                "reward": "greater_health_potion"
            }
        ),
        # ... (rest of the NPCs)
    }
    return npcs

# Define enemies
def create_game_enemies():
    enemies = {
        "wolf": Enemy(
            "Wolf", 
            "A fierce wolf with matted gray fur and sharp teeth.",
            20, 8, 
            loot=["health_potion"]
        ),
        # ... (rest of the enemies)
    }
    return enemies

# Game function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Typewriter effect for text
def print_slow(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Display game header
def display_header(game_state):
    clear_screen()
    print("=" * 80)
    print(f"ADVENTURES OF {game_state.player['name'].upper()}")
    print(f"Health: {game_state.player['health']}/{game_state.player['max_health']} | " +
          f"Location: {game_state.current_location} | " +
          f"Time: {game_state.game_time // 60}h {game_state.game_time % 60}m")
    print("=" * 80)
    print()

# Start a new game
def new_game():
    game_state = GameState()
    
    clear_screen()
    print_slow("Welcome to ADVENTURE QUEST!", 0.05)
    print_slow("A text-based adventure game full of exploration and danger.", 0.03)
    print()
    
    name = input("Enter your character's name: ")
    game_state.player["name"] = name if name else "Adventurer"
    
    print_slow(f"\nWelcome, {game_state.player['name']}! Your adventure begins in the village of Oakvale.")
    time.sleep(1)
    
    # Give the player some starting items
    game_state.player["inventory"].append("rusty_sword")
    game_state.player["equipped_weapon"] = "rusty_sword"
    game_state.player["inventory"].append("health_potion")
    
    return game_state

# Display location information
def display_location(game_state, world, npcs, enemies_dict):
    location = world[game_state.current_location]
    display_header(game_state)
    
    if game_state.current_location not in game_state.visited_locations:
        print_slow(f"You have arrived at {location['name']}.", 0.03)
        print_slow(location['description'], 0.03)
        game_state.visited_locations.add(game_state.current_location)
    else:
        print(f"You are at {location['name']}.")
        print(location['description'])
    
    print("\nYou can go to:")
    for connection in location['connections']:
        connected_location = world[connection]
        # Check if this connection requires an item
        if 'requires_item' in connected_location and connected_location['requires_item'] not in game_state.player['inventory']:
            print(f"- {connected_location['name']} (locked)")
        else:
            print(f"- {connected_location['name']}")
    
    if location['npcs']:
        print("\nPeople here:")
        for npc_id in location['npcs']:
            npc = npcs.get(npc_id)
            if npc:
                print(f"- {npc.name} ({npc_id})")
    
    if location['enemies']:
        print("\nEnemies here:")
        for enemy_id in location['enemies']:
            enemy = enemies_dict.get(enemy_id)
            if enemy:
                print(f"- {enemy.name}")
    
    if location['items']:
        print("\nItems here:")
        for item_id in location['items']:
            print(f"- {item_id}")
    
    print("\nWhat would you like to do?")

# Process player command
def process_command(command, game_state, world, items, npcs, enemies_dict):
    command = command.lower().strip()
    words = command.split()
    
    if not words:
        return
    
    action = words[0]
    target = " ".join(words[1:]) if len(words) > 1 else ""
    
    current_location = world.get(game_state.current_location)
    
    if current_location is None:
        return "Invalid location."

    # Movement commands
    if action in ["go", "move", "travel"]:
        for connection in current_location.get('connections', []):
            connected_location = world[connection]
            if target.lower() in connection.lower() or target.lower() in connected_location['name'].lower():
                # Check if location requires an item
                if 'requires_item' in connected_location:
                    required_item = connected_location['requires_item']
                    if required_item not in game_state.player['inventory']:
                        print_slow(f"You need a {required_item.replace('_', ' ')} to enter {connected_location['name']}.")
                        return
                
                game_state.current_location = connection
                game_state.game_time += 10  # Travel takes time
                return
        print_slow("You can't go there from here.")
    
    # Look command
    elif action in ["look", "examine"]:
        if not target:
            print_slow(current_location['description'])
        else:
            for item_id in current_location['items']:
                if target.lower() in item_id.lower() or (item_id in items and target.lower() in items[item_id].name.lower()):
                    if item_id in items:
                        print_slow(f"{items[item_id].name}: {items[item_id].description}")
                        return
            
            for npc_id in current_location['npcs']:
                if target.lower() in npc_id.lower() or (npc_id in npcs and target.lower() in npcs[npc_id].name.lower()):
                    if npc_id in npcs:
                        print_slow(f"{npcs[npc_id].name}: {npcs[npc_id].description}")
                        return
            
            for enemy_id in current_location['enemies']:
                if target.lower() in enemy_id.lower() or (enemy_id in enemies_dict and target.lower() in enemies_dict[enemy_id].name.lower()):
                    if enemy_id in enemies_dict:
                        print_slow(f"{enemies_dict[enemy_id].name}: {enemies_dict[enemy_id].description}")
                        return
            
            print_slow("You don't see that here.")
    
    # Take command
    elif action in ["take", "get", "pickup"]:
        for item_id in current_location['items'][:]:  # Create a copy to safely modify the original
            if target.lower() in item_id.lower() or (item_id in items and target.lower() in items[item_id].name.lower()):
                current_location['items'].remove(item_id)
                game_state.player['inventory'].append(item_id)
                if item_id in items:
                    print_slow(f"You picked up {items[item_id].name}.")
                else:
                    print_slow(f"You picked up {item_id.replace('_', ' ')}.")
                return
        print_slow("You don't see that here.")
    
    # Inventory command
    elif action in ["inventory", "i", "items"]:
        if not game_state.player['inventory']:
            print_slow("Your inventory is empty.")
        else:
            print_slow("You are carrying:")
            for item_id in game_state.player['inventory']:
                if item_id in items:
                    equipped = ""
                    if game_state.player['equipped_weapon'] == item_id:
                        equipped = " (equipped weapon)"
                    elif game_state.player['equipped_armor'] == item_id:
                        equipped = " (equipped armor)"
                    print(f"- {items[item_id].name}{equipped}")
                else:
                    print(f"- {item_id.replace('_', ' ')}")
    
    # Equip command
    elif action in ["equip", "wear", "wield"]:
        for item_id in game_state.player['inventory']:
            if target.lower() in item_id.lower() or (item_id in items and target.lower() in items[item_id].name.lower()):
                if item_id in items:
                    if items[item_id].item_type == "weapon":
                        game_state.player['equipped_weapon'] = item_id
                        print_slow(f"You equipped {items[item_id].name} as your weapon.")
                    elif items[item_id].item_type == "armor":
                        game_state.player['equipped_armor'] = item_id
                        print_slow(f"You equipped {items[item_id].name} as your armor.")
                    else:
                        print_slow(f"You can't equip {items[item_id].name}.")
                return
        print_slow("You don't have that item.")
    
    # Use command
    elif action in ["use", "drink", "consume"]:
        for item_id in game_state.player['inventory'][:]:  # Create a copy to safely modify
            if target.lower() in item_id.lower() or (item_id in items and target.lower() in items[item_id].name.lower()):
                if item_id in items:
                    if items[item_id].item_type == "potion":
                        game_state.player['inventory'].remove(item_id)
                        heal_amount = items[item_id].value
                        game_state.player['health'] = min(game_state.player['health'] + heal_amount, game_state.player['max_health'])
                        print_slow(f"You used {items[item_id].name} and recovered {heal_amount} health points.")
                    else:
                        print_slow(f"You can't use {items[item_id].name} that way.")
                return
        print_slow("You don't have that item.")
    
    # Talk command
    elif action in ["talk", "speak"]:
        for npc_id in current_location['npcs']:
            if target.lower() in npc_id.lower() or (npc_id in npcs and target.lower() in npcs[npc_id].name.lower()):
                if npc_id in npcs:
                    npc = npcs[npc_id]
                    print_slow(f"{npc.name}: \"{npc.dialogue['greeting']}\"")
                    
                    # Check if NPC has a quest
                    if npc.quest:
                        print_slow(f"\n{npc.name} has a quest for you: {npc.quest['name']}")
                        print_slow(npc.quest['description'])
                        
                        # Quest logic would go here
                    
                    # Check if NPC has trades
                    if npc.trades:
                        print_slow(f"\n{npc.name} can trade with you:")
                        for trade in npc.trades:
                            print(f"- {items[trade['give']].name} (costs {trade['cost']} gold)")
                return
        print_slow("There's no one by that name here.")
    
    # Attack command
    elif action in ["attack", "fight"]:
        for enemy_id in current_location['enemies'][:]:  # Create a copy to safely modify
            if target.lower() in enemy_id.lower() or (enemy_id in enemies_dict and target.lower() in enemies_dict[enemy_id].name.lower()):
                if enemy_id in enemies_dict:
                    enemy = enemies_dict[enemy_id]
                    enhanced_combat(game_state, enemy, current_location, enemy_id, items)
                return
        print_slow("There's no enemy by that name here.")
    
    # Help command
    elif action in ["help", "commands"]:
        print_slow("Available commands:")
        print_slow("- go/move/travel [location]: Move to a connected location")
        print_slow("- look/examine [object/person]: Look at something or someone")
        print_slow("- take/get/pickup [item]: Pick up an item")
        print_slow("- inventory/i/items: Check your inventory")
        print_slow("- equip/wear/wield [item]: Equip a weapon or armor")
        print_slow("- use/drink/consume [item]: Use an item like a potion")
        print_slow("- talk/speak [person]: Talk to an NPC")
        print_slow("- attack/fight [enemy]: Attack an enemy")
        print_slow("- help/commands: Show this help message")
        print_slow("- quit/exit: Exit the game")
    
    # Quit command
    elif action in ["quit", "exit"]:
        return "quit"
    
    else:
        print_slow("I don't understand that command. Type 'help' for a list of commands.")

# Enhanced combat system
def enhanced_combat(game_state, enemy, location, enemy_id, items):
    enemy_instance = Enemy(
        enemy.name,
        enemy.description,
        enemy.health,
        enemy.damage,
        enemy.loot.copy() if enemy.loot else []
    )
    
    print_slow(f"You engage in combat with {enemy_instance.name}!")
    
    player_weapon_damage = 2  # Bare hands
    if game_state.player['equipped_weapon'] and game_state.player['equipped_weapon'] in items:
        player_weapon_damage = items[game_state.player['equipped_weapon']].value
    
    player_armor = 0
    if game_state.player['equipped_armor'] and game_state.player['equipped_armor'] in items:
        player_armor = items[game_state.player['equipped_armor']].value
    
    # Combat status effects
    player_status = {
        "bleeding": 0,
        "poisoned": 0,
        "strengthened": 0
    }
    
    enemy_status = {
        "bleeding": 0,
        "poisoned": 0,
        "weakened": 0
    }
    
    turn = 1
    
    while enemy_instance.health > 0 and game_state.player['health'] > 0:
        clear_screen()
        print(f"=== COMBAT: TURN {turn} ===")
        print(f"You: Health {game_state.player['health']}/{game_state.player['max_health']}")
        print(f"{enemy_instance.name}: Health {max(0, enemy_instance.health)}")
        
        # Show status effects
        status_text = ""
        for status, duration in player_status.items():
            if duration > 0:
                status_text += f"{status.title()} ({duration}), "
        if status_text:
            print(f"Your status: {status_text[:-2]}")
        
        enemy_status_text = ""
        for status, duration in enemy_status.items():
            if duration > 0:
                enemy_status_text += f"{status.title()} ({duration}), "
        if enemy_status_text:
            print(f"Enemy status: {enemy_status_text[:-2]}")
        
        print("\nActions:")
        print("1. Attack - Basic attack with your weapon")
        print("2. Special Attack - Stronger attack with a chance to miss")
        print("3. Defend - Reduce incoming damage this turn")
        print("4. Use Item - Use a potion or other item")
        print("5. Flee - Attempt to escape combat")
        
        choice = input("\nChoose your action (1-5): ")
        
        # Apply status effects at start of turn
        if player_status["bleeding"] > 0:
            bleed_damage = random.randint(1, 3)
            game_state.player['health'] -= bleed_damage
            print_slow(f"You take {bleed_damage} bleeding damage.")
            player_status["bleeding"] -= 1
        
        if player_status["poisoned"] > 0:
            poison_damage = random.randint(2, 4)
            game_state.player['health'] -= poison_damage
            print_slow(f"You take {poison_damage} poison damage.")
            player_status["poisoned"] -= 1
        
        if enemy_status["bleeding"] > 0:
            bleed_damage = random.randint(1, 3)
            enemy_instance.health -= bleed_damage
            print_slow(f"{enemy_instance.name} takes {bleed_damage} bleeding damage.")
            enemy_status["bleeding"] -= 1
        
        if enemy_status["poisoned"] > 0:
            poison_damage = random.randint(2, 4)
            enemy_instance.health -= poison_damage
            print_slow(f"{enemy_instance.name} takes {poison_damage} poison damage.")
            enemy_status["poisoned"] -= 1
        
        # Check if either combatant died from status effects
        if game_state.player['health'] <= 0:
            print_slow("You have been defeated by your wounds!")
            return
        
        if enemy_instance.health <= 0:
            print_slow(f"Your {player_status} caused {enemy_instance.name} to collapse!")
            handle_enemy_defeat(game_state, enemy_instance, location, enemy_id, items)
            return
        
        # Player's action
        defending = False
        
        if choice == "1":  # Basic attack
            print_slow(f"You attack {enemy_instance.name} with your {game_state.player['equipped_weapon'].replace('_', ' ') if game_state.player['equipped_weapon'] else 'fists'}!")
            
            # Calculate damage with some randomness and status effects
            damage_modifier = 1.5 if player_status["strengthened"] > 0 else 1.0
            player_damage = max(1, int((player_weapon_damage + random.randint(-2, 2)) * damage_modifier))
            
            # Apply enemy weakened status
            if enemy_status["weakened"] > 0:
                player_damage = int(player_damage * 1.5)
            
            enemy_instance.health -= player_damage
            print_slow(f"You deal {player_damage} damage to {enemy_instance.name}.")
            
            # 10% chance to cause bleeding
            if random.random() < 0.1:
                enemy_status["bleeding"] = 3
                print_slow(f"Your attack causes {enemy_instance.name} to bleed!")
        
        elif choice == "2":  # Special attack
            print_slow(f"You prepare a special attack!")
            
            # 70% chance to hit, but higher damage
            if random.random() < 0.7:
                damage_modifier = 1.5 if player_status["strengthened"] > 0 else 1.0
                player_damage = max(1, int((player_weapon_damage * 2 + random.randint(-1, 3)) * damage_modifier))
                
                # Apply enemy weakened status
                if enemy_status["weakened"] > 0:
                    player_damage = int(player_damage * 1.5)
                
                enemy_instance.health -= player_damage
                print_slow(f"Your special attack hits for {player_damage} damage!")
                
                # 25% chance to cause bleeding or weaken
                if random.random() < 0.25:
                    effect = random.choice(["bleeding", "weakened"])
                    enemy_status[effect] = 3
                    print_slow(f"Your special attack causes {enemy_instance.name} to be {effect}!")
            else:
                print_slow("Your special attack misses!")
        
        elif choice == "3":  # Defend
            print_slow("You take a defensive stance.")
            defending = True
            
            # 25% chance to gain strength next turn
            if random.random() < 0.25:
                player_status["strengthened"] = 2
                print_slow("You find an opening in the enemy's attack pattern!")
        
        elif choice == "4":  # Use item
            print_slow("Your inventory:")
            usable_items = []
            
            for i, item_id in enumerate(game_state.player['inventory']):
                if item_id in items and items[item_id].item_type == "potion":
                    print(f"{i+1}. {items[item_id].name}")
                    usable_items.append(item_id)
            
            if not usable_items:
                print_slow("You don't have any usable items!")
            else:
                item_choice = input("Choose an item to use (or 0 to cancel): ")
                
                try:
                    item_index = int(item_choice) - 1
                    if 0 <= item_index < len(usable_items):
                        item_id = usable_items[item_index]
                        game_state.player['inventory'].remove(item_id)
                        
                        if "health_potion" in item_id:
                            heal_amount = items[item_id].value
                            game_state.player['health'] = min(game_state.player['health'] + heal_amount, game_state.player['max_health'])
                            print_slow(f"You used {items[item_id].name} and recovered {heal_amount} health points.")
                        
                        # Skip enemy turn this round since we used an item
                        turn += 1
                        continue
                except:
                    print_slow("Invalid choice.")
        
        elif choice == "5":  # Flee
            print_slow("You attempt to flee from combat!")
            
            # Calculate flee chance (higher at lower health)
            flee_chance = 0.4 + (1 - game_state.player['health'] / game_state.player['max_health']) * 0.3
            
            if random.random() < flee_chance:
                print_slow("You successfully escape!")
                game_state.game_time += 5
                return
            else:
                print_slow("You failed to escape!")
        
        # Check if enemy is defeated after player action
        if enemy_instance.health <= 0:
            handle_enemy_defeat(game_state, enemy_instance, location, enemy_id, items)
            return
        
        # Enemy's turn
        print_slow(f"\n{enemy_instance.name} attacks you!")
        
        # Calculate enemy damage
        enemy_damage = max(1, enemy_instance.damage + random.randint(-2, 2) - player_armor)
        
        # Reduce damage if defending
        if defending:
            enemy_damage = max(1, int(enemy_damage * 0.5))
            print_slow("Your defensive stance reduces the damage!")
        
        # Apply damage
        game_state.player['health'] -= enemy_damage
        print_slow(f"{enemy_instance.name} deals {enemy_damage} damage to you.")
        
        # Special enemy effects
        if random.random() < 0.15:  # 15% chance for status effect
            effect = random.choice(["bleeding", "poisoned"])
            player_status[effect] = 3
            print_slow(f"The attack causes you to be {effect}!")
        
        # Check if player is defeated
        if game_state.player['health'] <= 0:
            print_slow("You have been defeated!")
            return
        
        # Wait for player to continue
        input("\nPress Enter to continue...")
        turn += 1

# Handle enemy defeat
def handle_enemy_defeat(game_state, enemy, location, enemy_id, items):
    print_slow(f"You defeated {enemy.name}!")
    
    # Give rewards
    if enemy.loot:
        print_slow("You found:")
        for loot_item in enemy.loot:
            game_state.player['inventory'].append(loot_item)
            if loot_item in items:
                print_slow(f"- {items[loot_item].name}")
            else:
                print_slow(f"- {loot_item.replace('_', ' ')}")
    
    # Remove enemy from location
    if enemy_id in location['enemies']:
        location['enemies'].remove(enemy_id)
    
    # Update quest progress if applicable
    if enemy_id == "wolf" and "forest_cleared" in game_state.quest_progress:
        game_state.quest_progress["forest_cleared"] = True
    
    if enemy_id == "mine_guardian" and "mines_cleared" in game_state.quest_progress:
        game_state.quest_progress["mines_cleared"] = True
    
    game_state.enemies_defeated += 1
    game_state.game_time += 5  # Combat takes time

# Main game loop
def main_game_loop():
    game_state = new_game()
    world = create_game_world()
    items = create_game_items()
    npcs = create_game_npcs()
    enemies_dict = create_game_enemies()
    
    running = True
    while running:
        display_location(game_state, world, npcs, enemies_dict)
        
        command = input("> ")
        result = process_command(command, game_state, world, items, npcs, enemies_dict)
        
        if result == "quit":
            print_slow("Thank you for playing Adventure Quest!")
            running = False
        
        # Check if player is dead
        if game_state.player['health'] <= 0:
            print_slow("You have been defeated! Game Over!")
            choice = input("Would you like to play again? (y/n): ")
            if choice.lower() == 'y':
                game_state = new_game()
            else:
                print_slow("Thank you for playing Adventure Quest!")
                running = False
        
        # Check for game completion
        if game_state.current_location == "throne_room" and "dark_knight" not in world["throne_room"]["enemies"]:
            display_victory(game_state)
            choice = input("Would you like to play again? (y/n): ")
            if choice.lower() == 'y':
                game_state = new_game()
            else:
                print_slow("Thank you for playing Adventure Quest!")
                running = False
        
        # Advance game time
        game_state.game_time += 1
        
        # Auto-heal slightly over time
        if game_state.game_time % 10 == 0 and game_state.player['health'] < game_state.player['max_health']:
            game_state.player['health'] = min(game_state.player['health'] + 1, game_state.player['max_health'])

# Display victory message
def display_victory(game_state):
    clear_screen()
    print("=" * 80)
    print("VICTORY!")
    print("=" * 80)
    print_slow(f"Congratulations, {game_state.player['name']}! You have defeated the Dark Knight and saved the kingdom!", 0.05)
    print_slow("The people celebrate your heroism, and the king awards you with the highest honor.", 0.03)
    print()
    print(f"Final stats:")
    print(f"- Enemies defeated: {game_state.enemies_defeated}")
    print(f"- Game time: {game_state.game_time // 60}h {game_state.game_time % 60}m")
    print(f"- Locations visited: {len(game_state.visited_locations)}")
    print()
    print_slow("The End", 0.1)
    print()

# Save game function (simplified)
def save_game(game_state):
    try:
        # In a real game, you'd serialize the game state to a file
        print_slow("Game saved successfully!")
        return True
    except:
        print_slow("Failed to save game.")
        return False

# Load game function (simplified)
def load_game():
    try:
        # In a real game, you'd deserialize from a file
        print_slow("No saved game found.")
        return None
    except:
        print_slow("Failed to load game.")
        return None

# Title screen
def title_screen():
    clear_screen()
    print("=" * 80)
    print(" " * 30 + "ADVENTURE QUEST")
    print("=" * 80)
    print_slow("A text-based adventure game full of danger and mystery.", 0.03)
    print()
    print("1. New Game")
    print("2. Load Game")
    print("3. About")
    print("4. Quit")
    print()
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        return main_game_loop()
    elif choice == "2":
        game_state = load_game()
        if game_state:
            return main_game_loop(game_state)
        else:
            return title_screen()
    elif choice == "3":
        about_screen()
        return title_screen()
    elif choice == "4":
        print_slow("Thank you for playing Adventure Quest!")
        return
    else:
        print_slow("Invalid choice. Please try again.")
        time.sleep(1)
        return title_screen()

# About screen
def about_screen():
    clear_screen()
    print("=" * 80)
    print(" " * 30 + "ABOUT")
    print("=" * 80)
    print_slow("Adventure Quest is a text-based RPG adventure game.", 0.03)
    print_slow("Explore the world, complete quests, fight monsters, and save the kingdom!", 0.03)
    print()
    print_slow("How to play:", 0.03)
    print("- Type commands to interact with the game world")
    print("- Use 'help' to see a list of available commands")
    print("- Explore different locations, talk to NPCs, and collect items")
    print("- Defeat enemies to progress in the game")
    print()
    print_slow("Press Enter to return to the title screen...", 0.03)
    input()

# Class for quests
class Quest:
    def __init__(self, name, description, objectives, reward):
        self.name = name
        self.description = description
        self.objectives = objectives  # List of objectives
        self.completed_objectives = []
        self.reward = reward
        self.completed = False
    
    def update_objective(self, objective):
        if objective in self.objectives and objective not in self.completed_objectives:
            self.completed_objectives.append(objective)
            return True
        return False
    
    def check_completion(self):
        if set(self.objectives) <= set(self.completed_objectives) and not self.completed:
            self.completed = True
            return True
        return False

# Create game quests
def create_game_quests():
    quests = {
        "village_troubles": Quest(
            "Village Troubles",
            "Investigate the forest and abandoned mines to discover what's causing problems for the village.",
            ["clear_forest", "clear_mines"],
            "greater_health_potion"
        ),
        "royal_amulet": Quest(
            "The Royal Amulet",
            "Find the ancient amulet and bring it to the castle to help stop the darkness.",
            ["find_amulet", "deliver_amulet"],
            "enchanted_blade"
        )
    }
    return quests

# Handle specific quest updates based on player actions
def update_quests(game_state, quest_id, objective):
    if quest_id in game_state.quests and objective in game_state.quests[quest_id].objectives:
        if game_state.quests[quest_id].update_objective(objective):
            print_slow(f"Quest objective completed: {objective.replace('_', ' ').title()}")
            
            if game_state.quests[quest_id].check_completion():
                print_slow(f"Quest completed: {game_state.quests[quest_id].name}")
                reward = game_state.quests[quest_id].reward
                game_state.player['inventory'].append(reward)
                print_slow(f"You received: {reward.replace('_', ' ').title()}")
                return True
    return False

# Main function
if __name__ == "__main__":
    try:
        title_screen()
    except KeyboardInterrupt:
        print("\nGame exited.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to exit...")