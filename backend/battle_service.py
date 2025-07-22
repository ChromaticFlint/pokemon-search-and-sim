import random
import math

# Type emojis for battle log
TYPE_EMOJIS = {
    "normal": "⚪",
    "fire": "🔥",
    "water": "💧",
    "electric": "⚡",
    "grass": "🌿",
    "ice": "❄️",
    "fighting": "👊",
    "poison": "☠️",
    "ground": "🌍",
    "flying": "🌪️",
    "psychic": "🔮",
    "bug": "🐛",
    "rock": "🗿",
    "ghost": "👻",
    "dragon": "🐉",
    "dark": "🌑",
    "steel": "⚙️",
    "fairy": "✨"
}

def get_type_emoji(pokemon_type):
    """Get emoji for Pokemon type"""
    return TYPE_EMOJIS.get(pokemon_type, "⚔️")

# Pokemon type effectiveness chart
TYPE_EFFECTIVENESS = {
    "normal": {
        "rock": 0.5, "ghost": 0, "steel": 0.5
    },
    "fire": {
        "fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2
    },
    "water": {
        "fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5
    },
    "electric": {
        "water": 2, "electric": 0.5, "grass": 0.5, "ground": 0, "flying": 2, "dragon": 0.5
    },
    "grass": {
        "fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2, "dragon": 0.5, "steel": 0.5
    },
    "ice": {
        "fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2, "dragon": 2, "steel": 0.5
    },
    "fighting": {
        "normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0, "dark": 2, "steel": 2, "fairy": 0.5
    },
    "poison": {
        "grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0, "fairy": 2
    },
    "ground": {
        "fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "flying": 0, "bug": 0.5, "rock": 2, "steel": 2
    },
    "flying": {
        "electric": 0.5, "grass": 2, "ice": 0.5, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5
    },
    "psychic": {
        "fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5
    },
    "bug": {
        "fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2, "ghost": 0.5, "dark": 2, "steel": 0.5, "fairy": 0.5
    },
    "rock": {
        "fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2, "steel": 0.5
    },
    "ghost": {
        "normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5
    },
    "dragon": {
        "dragon": 2, "steel": 0.5, "fairy": 0
    },
    "dark": {
        "fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5, "fairy": 0.5
    },
    "steel": {
        "fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2, "rock": 2, "steel": 0.5, "fairy": 2
    },
    "fairy": {
        "fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2, "dark": 2, "steel": 0.5
    }
}

def get_type_effectiveness(attacking_type, defending_types):
    """Calculate type effectiveness multiplier"""
    if attacking_type not in TYPE_EFFECTIVENESS:
        return 1.0

    multiplier = 1.0
    for defending_type in defending_types:
        if defending_type in TYPE_EFFECTIVENESS[attacking_type]:
            multiplier *= TYPE_EFFECTIVENESS[attacking_type][defending_type]

    return multiplier

# Enhanced move database with accuracy, effects, and critical hit ratios
MOVE_DATABASE = {
    # Electric moves
    "thunderbolt": {"name": "Thunderbolt", "power": 90, "type": "electric", "category": "special", "accuracy": 100, "effect": "paralysis", "effect_chance": 10, "crit_ratio": 1},
    "thunder": {"name": "Thunder", "power": 110, "type": "electric", "category": "special", "accuracy": 70, "effect": "paralysis", "effect_chance": 30, "crit_ratio": 1},
    "wild_charge": {"name": "Wild Charge", "power": 90, "type": "electric", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},

    # Water moves
    "hydro_pump": {"name": "Hydro Pump", "power": 110, "type": "water", "category": "special", "accuracy": 80, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "surf": {"name": "Surf", "power": 90, "type": "water", "category": "special", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "aqua_tail": {"name": "Aqua Tail", "power": 90, "type": "water", "category": "physical", "accuracy": 90, "effect": None, "effect_chance": 0, "crit_ratio": 1},

    # Fire moves
    "flamethrower": {"name": "Flamethrower", "power": 90, "type": "fire", "category": "special", "accuracy": 100, "effect": "burn", "effect_chance": 10, "crit_ratio": 1},
    "fire_blast": {"name": "Fire Blast", "power": 110, "type": "fire", "category": "special", "accuracy": 85, "effect": "burn", "effect_chance": 10, "crit_ratio": 1},
    "flare_blitz": {"name": "Flare Blitz", "power": 120, "type": "fire", "category": "physical", "accuracy": 100, "effect": "burn", "effect_chance": 10, "crit_ratio": 1},

    # Grass moves
    "solar_beam": {"name": "Solar Beam", "power": 120, "type": "grass", "category": "special", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "leaf_storm": {"name": "Leaf Storm", "power": 130, "type": "grass", "category": "special", "accuracy": 90, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "wood_hammer": {"name": "Wood Hammer", "power": 120, "type": "grass", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},

    # Psychic moves
    "psychic": {"name": "Psychic", "power": 90, "type": "psychic", "category": "special", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "psybeam": {"name": "Psybeam", "power": 65, "type": "psychic", "category": "special", "accuracy": 100, "effect": "confusion", "effect_chance": 10, "crit_ratio": 1},

    # Ice moves
    "ice_beam": {"name": "Ice Beam", "power": 90, "type": "ice", "category": "special", "accuracy": 100, "effect": "freeze", "effect_chance": 10, "crit_ratio": 1},
    "blizzard": {"name": "Blizzard", "power": 110, "type": "ice", "category": "special", "accuracy": 70, "effect": "freeze", "effect_chance": 10, "crit_ratio": 1},

    # Dragon moves
    "dragon_pulse": {"name": "Dragon Pulse", "power": 85, "type": "dragon", "category": "special", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "dragon_claw": {"name": "Dragon Claw", "power": 80, "type": "dragon", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},

    # Dark moves
    "dark_pulse": {"name": "Dark Pulse", "power": 80, "type": "dark", "category": "special", "accuracy": 100, "effect": "flinch", "effect_chance": 20, "crit_ratio": 1},
    "crunch": {"name": "Crunch", "power": 80, "type": "dark", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},

    # Normal moves
    "hyper_beam": {"name": "Hyper Beam", "power": 150, "type": "normal", "category": "special", "accuracy": 90, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "body_slam": {"name": "Body Slam", "power": 85, "type": "normal", "category": "physical", "accuracy": 100, "effect": "paralysis", "effect_chance": 30, "crit_ratio": 1},

    # Fighting moves
    "close_combat": {"name": "Close Combat", "power": 120, "type": "fighting", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "focus_blast": {"name": "Focus Blast", "power": 120, "type": "fighting", "category": "special", "accuracy": 70, "effect": None, "effect_chance": 0, "crit_ratio": 1},

    # Other types
    "earthquake": {"name": "Earthquake", "power": 100, "type": "ground", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "stone_edge": {"name": "Stone Edge", "power": 100, "type": "rock", "category": "physical", "accuracy": 80, "effect": None, "effect_chance": 0, "crit_ratio": 3},  # High crit ratio
    "shadow_ball": {"name": "Shadow Ball", "power": 80, "type": "ghost", "category": "special", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 1},

    # High critical hit moves
    "slash": {"name": "Slash", "power": 70, "type": "normal", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 3},
    "psycho_cut": {"name": "Psycho Cut", "power": 70, "type": "psychic", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 3},
    "night_slash": {"name": "Night Slash", "power": 70, "type": "dark", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 3},
    "leaf_blade": {"name": "Leaf Blade", "power": 90, "type": "grass", "category": "physical", "accuracy": 100, "effect": None, "effect_chance": 0, "crit_ratio": 3},

    # Low accuracy moves
    "focus_blast": {"name": "Focus Blast", "power": 120, "type": "fighting", "category": "special", "accuracy": 70, "effect": None, "effect_chance": 0, "crit_ratio": 1},
    "dynamic_punch": {"name": "Dynamic Punch", "power": 100, "type": "fighting", "category": "physical", "accuracy": 50, "effect": "confusion", "effect_chance": 100, "crit_ratio": 1},
    "zap_cannon": {"name": "Zap Cannon", "power": 120, "type": "electric", "category": "special", "accuracy": 50, "effect": "paralysis", "effect_chance": 100, "crit_ratio": 1},

    # Status moves
    "toxic": {"name": "Toxic", "power": None, "type": "poison", "category": "status", "accuracy": 90, "effect": "poison", "effect_chance": 100, "crit_ratio": 1},
    "sleep_powder": {"name": "Sleep Powder", "power": None, "type": "grass", "category": "status", "accuracy": 75, "effect": "sleep", "effect_chance": 100, "crit_ratio": 1},
    "thunder_wave": {"name": "Thunder Wave", "power": None, "type": "electric", "category": "status", "accuracy": 90, "effect": "paralysis", "effect_chance": 100, "crit_ratio": 1},

    # Poison moves
    "sludge_bomb": {"name": "Sludge Bomb", "power": 90, "type": "poison", "category": "special", "accuracy": 100, "effect": "poison", "effect_chance": 30, "crit_ratio": 1},
}

# Pokemon-specific movesets (4 moves each)
POKEMON_MOVESETS = {
    "pikachu": ["thunderbolt", "thunder", "body_slam", "wild_charge"],
    "charizard": ["flamethrower", "fire_blast", "dragon_claw", "earthquake"],
    "blastoise": ["hydro_pump", "surf", "ice_beam", "earthquake"],
    "venusaur": ["solar_beam", "leaf_storm", "earthquake", "sludge_bomb"],
    "gyarados": ["hydro_pump", "earthquake", "crunch", "thunder"],
    "dragonite": ["dragon_pulse", "dragon_claw", "thunder", "earthquake"],
    "mewtwo": ["psychic", "psybeam", "shadow_ball", "fire_blast"],
    "mew": ["psychic", "thunderbolt", "flamethrower", "ice_beam"],
    # Add more as needed - fallback to type-based moves
}

# Status effects
STATUS_EFFECTS = {
    "paralysis": {"name": "Paralysis", "emoji": "⚡", "duration": 3, "damage_per_turn": 0, "speed_reduction": 0.5},
    "burn": {"name": "Burn", "emoji": "🔥", "duration": 3, "damage_per_turn": 0.125, "speed_reduction": 0},  # 1/8 max HP per turn
    "freeze": {"name": "Freeze", "emoji": "❄️", "duration": 2, "damage_per_turn": 0, "speed_reduction": 0},
    "confusion": {"name": "Confusion", "emoji": "😵", "duration": 2, "damage_per_turn": 0, "speed_reduction": 0},
}

def calculate_level_stats(base_stats, level):
    """Calculate Pokemon stats at a given level using the standard formula"""
    # Pokemon stat formula: ((2 * base + IV + EV/4) * level / 100) + 5
    # Simplified: assume perfect IVs (31) and no EVs for fairness
    calculated_stats = []

    for i, base_stat in enumerate(base_stats):
        if i == 0:  # HP has a different formula
            stat = int(((2 * base_stat + 31) * level / 100) + level + 10)
        else:  # Other stats
            stat = int(((2 * base_stat + 31) * level / 100) + 5)
        calculated_stats.append(stat)

    return calculated_stats

def get_pokemon_moveset(pokemon_name, pokemon_types, attacker_stats):
    """Get Pokemon's moveset - either specific or type-based"""
    pokemon_name_lower = pokemon_name.lower()

    # Check if we have a specific moveset for this Pokemon
    if pokemon_name_lower in POKEMON_MOVESETS:
        move_keys = POKEMON_MOVESETS[pokemon_name_lower]
        return [MOVE_DATABASE[key] for key in move_keys]

    # Fallback to type-based moveset
    primary_type = pokemon_types[0] if pokemon_types else "normal"
    secondary_type = pokemon_types[1] if len(pokemon_types) > 1 else None

    # Build moveset based on types and stats
    moveset = []

    # Primary type move
    if primary_type == "electric":
        moveset.append(MOVE_DATABASE["thunderbolt"])
    elif primary_type == "water":
        moveset.append(MOVE_DATABASE["surf"])
    elif primary_type == "fire":
        moveset.append(MOVE_DATABASE["flamethrower"])
    elif primary_type == "grass":
        moveset.append(MOVE_DATABASE["solar_beam"])
    elif primary_type == "psychic":
        moveset.append(MOVE_DATABASE["psychic"])
    elif primary_type == "ice":
        moveset.append(MOVE_DATABASE["ice_beam"])
    elif primary_type == "dragon":
        moveset.append(MOVE_DATABASE["dragon_pulse"])
    elif primary_type == "dark":
        moveset.append(MOVE_DATABASE["dark_pulse"])
    elif primary_type == "fighting":
        moveset.append(MOVE_DATABASE["close_combat"])
    else:
        moveset.append(MOVE_DATABASE["body_slam"])

    # Secondary type move (if exists)
    if secondary_type and secondary_type != primary_type:
        if secondary_type == "flying":
            moveset.append(MOVE_DATABASE["earthquake"])  # Coverage move
        elif secondary_type == "poison":
            moveset.append(MOVE_DATABASE["sludge_bomb"])
        else:
            moveset.append(MOVE_DATABASE["shadow_ball"])  # Neutral coverage
    else:
        # Add coverage move based on stats
        if attacker_stats[1] > attacker_stats[3]:  # Physical attacker
            moveset.append(MOVE_DATABASE["earthquake"])
        else:  # Special attacker
            moveset.append(MOVE_DATABASE["shadow_ball"])

    # Add two more moves for variety
    moveset.append(MOVE_DATABASE["body_slam"])  # Status move
    moveset.append(MOVE_DATABASE["stone_edge"])  # High crit move

    return moveset[:4]  # Limit to 4 moves

def select_move(moveset, turn_number):
    """Select a move from the Pokemon's moveset"""
    # Simple AI: cycle through moves with some randomness
    if turn_number <= 2:
        # Use strongest moves first
        return max(moveset, key=lambda m: m["power"])
    else:
        # Random selection for variety
        return random.choice(moveset)

def check_accuracy(move_data):
    """Check if move hits based on accuracy"""
    return random.randint(1, 100) <= move_data["accuracy"]

def check_critical_hit(move_data):
    """Check for critical hit based on move's crit ratio"""
    crit_chance = move_data["crit_ratio"] * 6.25  # Base 6.25% chance
    return random.randint(1, 1000) <= (crit_chance * 10)

def apply_status_effect(target_name, move_data, battle_log):
    """Apply status effect if move has one"""
    if move_data["effect"] and move_data["effect_chance"] > 0:
        if random.randint(1, 100) <= move_data["effect_chance"]:
            effect = STATUS_EFFECTS[move_data["effect"]]
            battle_log.append(f"{effect['emoji']} {target_name} is {effect['name'].lower()}!")
            return move_data["effect"]
    return None

def calculate_damage(attacker_stats, defender_stats, attacker_types, defender_types, move_data, level=50, is_critical=False):
    """Calculate damage using enhanced Pokemon damage formula"""
    # Choose attack and defense stats based on move category
    if move_data["category"] == "physical":
        attack_stat = attacker_stats[1]  # Attack
        defense_stat = defender_stats[2]  # Defense
    else:  # special
        attack_stat = attacker_stats[3]  # Special Attack
        defense_stat = defender_stats[4]  # Special Defense

    # Base damage calculation (Pokemon damage formula)
    power = move_data["power"]

    # Critical hits ignore defense boosts and deal 1.5x damage
    if is_critical:
        defense_stat = min(defense_stat, defender_stats[2] if move_data["category"] == "physical" else defender_stats[4])

    # Damage formula: ((((2 * Level / 5 + 2) * Power * Attack / Defense) / 50) + 2) * Modifiers
    damage = ((((2 * level / 5 + 2) * power * attack_stat / defense_stat) / 50) + 2)

    # Apply critical hit multiplier
    if is_critical:
        damage *= 1.5

    # Apply STAB (Same Type Attack Bonus) - 1.5x if move type matches Pokemon type
    if move_data["type"] in attacker_types:
        damage *= 1.5

    # Apply type effectiveness
    type_multiplier = get_type_effectiveness(move_data["type"], defender_types)
    damage *= type_multiplier

    # Add some randomness (85-100% of calculated damage)
    damage *= random.uniform(0.85, 1.0)

    return int(damage), type_multiplier, is_critical

def simulate_battle_advanced(pokemon_a_data, pokemon_b_data, level_a=50, level_b=50):
    """Enhanced battle simulation with movesets, status effects, and levels"""
    # Extract base stats
    base_stats_a = [
        pokemon_a_data['metadata']['stats']['hp'],
        pokemon_a_data['metadata']['stats']['attack'],
        pokemon_a_data['metadata']['stats']['defense'],
        pokemon_a_data['metadata']['stats']['special_attack'],
        pokemon_a_data['metadata']['stats']['special_defense'],
        pokemon_a_data['metadata']['stats']['speed']
    ]

    base_stats_b = [
        pokemon_b_data['metadata']['stats']['hp'],
        pokemon_b_data['metadata']['stats']['attack'],
        pokemon_b_data['metadata']['stats']['defense'],
        pokemon_b_data['metadata']['stats']['special_attack'],
        pokemon_b_data['metadata']['stats']['special_defense'],
        pokemon_b_data['metadata']['stats']['speed']
    ]

    # Calculate level-adjusted stats
    stats_a = calculate_level_stats(base_stats_a, level_a)
    stats_b = calculate_level_stats(base_stats_b, level_b)

    types_a = pokemon_a_data['metadata']['types']
    types_b = pokemon_b_data['metadata']['types']

    name_a = pokemon_a_data['name']
    name_b = pokemon_b_data['name']

    # Get movesets for each Pokemon
    moveset_a = get_pokemon_moveset(name_a, types_a, stats_a)
    moveset_b = get_pokemon_moveset(name_b, types_b, stats_b)

    # Initialize HP and status
    hp_a = stats_a[0]
    hp_b = stats_b[0]
    max_hp_a = hp_a
    max_hp_b = hp_b

    # Status effect tracking
    status_a = None
    status_b = None
    status_turns_a = 0
    status_turns_b = 0

    battle_log = []
    turn = 1

    battle_log.append(f"🥊 {name_a} (Lv.{level_a}) vs {name_b} (Lv.{level_b}) - Battle begins!")
    battle_log.append(f"📊 {name_a}: {hp_a} HP ({'/'.join(types_a)} type)")
    battle_log.append(f"📊 {name_b}: {hp_b} HP ({'/'.join(types_b)} type)")
    battle_log.append(f"🎯 {name_a}'s moves: {', '.join([move['name'] for move in moveset_a])}")
    battle_log.append(f"🎯 {name_b}'s moves: {', '.join([move['name'] for move in moveset_b])}")
    battle_log.append("")

    while hp_a > 0 and hp_b > 0 and turn <= 20:  # Max 20 turns to prevent infinite battles
        battle_log.append(f"--- Turn {turn} ---")

        # Determine turn order based on speed
        if stats_a[5] >= stats_b[5]:  # A goes first
            first_attacker, first_defender = (name_a, stats_a, types_a, 'a'), (name_b, stats_b, types_b, 'b')
            second_attacker, second_defender = (name_b, stats_b, types_b, 'b'), (name_a, stats_a, types_a, 'a')
        else:  # B goes first
            first_attacker, first_defender = (name_b, stats_b, types_b, 'b'), (name_a, stats_a, types_a, 'a')
            second_attacker, second_defender = (name_a, stats_a, types_a, 'a'), (name_b, stats_b, types_b, 'b')

        # First attack
        if (first_attacker[3] == 'a' and hp_a > 0) or (first_attacker[3] == 'b' and hp_b > 0):
            # Get moveset and select a move for this Pokemon
            moveset = get_pokemon_moveset(first_attacker[0], first_attacker[2], first_attacker[1])
            move_data = select_move(moveset, turn)

            # Check for critical hit and accuracy
            is_critical = check_critical_hit(move_data)
            if not check_accuracy(move_data):
                # Move missed
                battle_log.append(f"💨 {first_attacker[0]}'s {move_data['name']} missed!")
            else:
                damage, type_mult, _ = calculate_damage(first_attacker[1], first_defender[1], first_attacker[2], first_defender[2], move_data, level_a if first_attacker[3] == 'a' else level_b, is_critical)

                if first_attacker[3] == 'a':
                    hp_b -= damage
                    hp_b = max(0, hp_b)
                else:
                    hp_a -= damage
                    hp_a = max(0, hp_a)

                # Log the attack with move name
                effectiveness = ""
                if type_mult > 1:
                    effectiveness = " (Super effective!)"
                elif type_mult < 1 and type_mult > 0:
                    effectiveness = " (Not very effective...)"
                elif type_mult == 0:
                    effectiveness = " (No effect!)"

                # Add critical hit indicator
                crit_text = " (Critical hit!)" if is_critical else ""

                # Get type emoji
                type_emoji = get_type_emoji(move_data["type"])
                battle_log.append(f"{type_emoji} {first_attacker[0]} uses {move_data['name']}! {damage} damage{effectiveness}{crit_text}")

                # Apply status effect if any
                if first_defender[3] == 'a':
                    apply_status_effect(name_a, move_data, battle_log)
                    battle_log.append(f"💚 {name_a}: {hp_a}/{max_hp_a} HP remaining")
                else:
                    apply_status_effect(name_b, move_data, battle_log)
                    battle_log.append(f"💚 {name_b}: {hp_b}/{max_hp_b} HP remaining")

        # Check if battle is over
        if hp_a <= 0 or hp_b <= 0:
            break

        # Second attack
        if (second_attacker[3] == 'a' and hp_a > 0) or (second_attacker[3] == 'b' and hp_b > 0):
            # Get moveset and select a move for this Pokemon
            moveset = get_pokemon_moveset(second_attacker[0], second_attacker[2], second_attacker[1])
            move_data = select_move(moveset, turn)

            # Check for critical hit and accuracy
            is_critical = check_critical_hit(move_data)
            if not check_accuracy(move_data):
                # Move missed
                battle_log.append(f"💨 {second_attacker[0]}'s {move_data['name']} missed!")
            else:
                damage, type_mult, _ = calculate_damage(second_attacker[1], second_defender[1], second_attacker[2], second_defender[2], move_data, level_a if second_attacker[3] == 'a' else level_b, is_critical)

                if second_attacker[3] == 'a':
                    hp_b -= damage
                    hp_b = max(0, hp_b)
                else:
                    hp_a -= damage
                    hp_a = max(0, hp_a)

                effectiveness = ""
                if type_mult > 1:
                    effectiveness = " (Super effective!)"
                elif type_mult < 1 and type_mult > 0:
                    effectiveness = " (Not very effective...)"
                elif type_mult == 0:
                    effectiveness = " (No effect!)"

                # Add critical hit indicator
                crit_text = " (Critical hit!)" if is_critical else ""

                # Get type emoji
                type_emoji = get_type_emoji(move_data["type"])
                battle_log.append(f"{type_emoji} {second_attacker[0]} uses {move_data['name']}! {damage} damage{effectiveness}{crit_text}")

                # Apply status effect if any
                if second_defender[3] == 'a':
                    apply_status_effect(name_a, move_data, battle_log)
                    battle_log.append(f"💚 {name_a}: {hp_a}/{max_hp_a} HP remaining")
                else:
                    apply_status_effect(name_b, move_data, battle_log)
                    battle_log.append(f"💚 {name_b}: {hp_b}/{max_hp_b} HP remaining")

        battle_log.append("")
        turn += 1

    # Determine winner
    if hp_a <= 0 and hp_b <= 0:
        winner = "Draw! Both Pokemon fainted!"
        battle_log.append("🤝 It's a draw! Both Pokemon fainted!")
    elif hp_a <= 0:
        winner = f"{name_b} wins!"
        battle_log.append(f"🏆 {name_b} wins the battle!")
    elif hp_b <= 0:
        winner = f"{name_a} wins!"
        battle_log.append(f"🏆 {name_a} wins the battle!")
    else:
        winner = "Battle timed out (20 turns reached)"
        battle_log.append("⏰ Battle timed out after 20 turns!")

    return {
        "result": winner,
        "battle_log": battle_log,
        "final_hp": {"pokemon_a": hp_a, "pokemon_b": hp_b},
        "turns": turn - 1
    }

def simulate_battle(stats_a, stats_b):
    """Simple battle simulation (backwards compatibility)"""
    total_a = sum(stats_a)
    total_b = sum(stats_b)

    if total_a > total_b:
        return "Pokemon A wins"
    elif total_b > total_a:
        return "Pokemon B wins"
    else:
        return "Draw"
