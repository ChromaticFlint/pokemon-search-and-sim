import random
import math

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

def calculate_damage(attacker_stats, defender_stats, attacker_types, defender_types, is_physical=True):
    """Calculate damage using simplified Pokemon damage formula"""
    # Choose attack and defense stats
    if is_physical:
        attack_stat = attacker_stats[1]  # Attack
        defense_stat = defender_stats[2]  # Defense
        attack_type = attacker_types[0] if attacker_types else "normal"  # Use primary type
    else:
        attack_stat = attacker_stats[3]  # Special Attack
        defense_stat = defender_stats[4]  # Special Defense
        attack_type = attacker_types[0] if attacker_types else "normal"  # Use primary type

    # Base damage calculation (simplified)
    level = 50  # Assume level 50
    power = 80  # Assume moderate power move

    # Damage formula (simplified version of Pokemon damage calculation)
    damage = ((((2 * level / 5 + 2) * power * attack_stat / defense_stat) / 50) + 2)

    # Apply type effectiveness
    type_multiplier = get_type_effectiveness(attack_type, defender_types)
    damage *= type_multiplier

    # Add some randomness (85-100% of calculated damage)
    damage *= random.uniform(0.85, 1.0)

    return int(damage), type_multiplier

def simulate_battle_advanced(pokemon_a_data, pokemon_b_data):
    """Advanced battle simulation with type effectiveness"""
    # Extract data
    stats_a = [
        pokemon_a_data['metadata']['stats']['hp'],
        pokemon_a_data['metadata']['stats']['attack'],
        pokemon_a_data['metadata']['stats']['defense'],
        pokemon_a_data['metadata']['stats']['special_attack'],
        pokemon_a_data['metadata']['stats']['special_defense'],
        pokemon_a_data['metadata']['stats']['speed']
    ]

    stats_b = [
        pokemon_b_data['metadata']['stats']['hp'],
        pokemon_b_data['metadata']['stats']['attack'],
        pokemon_b_data['metadata']['stats']['defense'],
        pokemon_b_data['metadata']['stats']['special_attack'],
        pokemon_b_data['metadata']['stats']['special_defense'],
        pokemon_b_data['metadata']['stats']['speed']
    ]

    types_a = pokemon_a_data['metadata']['types']
    types_b = pokemon_b_data['metadata']['types']

    name_a = pokemon_a_data['name']
    name_b = pokemon_b_data['name']

    # Initialize HP
    hp_a = stats_a[0]
    hp_b = stats_b[0]
    max_hp_a = hp_a
    max_hp_b = hp_b

    battle_log = []
    turn = 1

    battle_log.append(f"🥊 {name_a} vs {name_b} - Battle begins!")
    battle_log.append(f"📊 {name_a}: {hp_a} HP ({'/'.join(types_a)} type)")
    battle_log.append(f"📊 {name_b}: {hp_b} HP ({'/'.join(types_b)} type)")
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
            # Choose physical or special attack based on higher stat
            is_physical = first_attacker[1][1] > first_attacker[1][3]
            damage, type_mult = calculate_damage(first_attacker[1], first_defender[1], first_attacker[2], first_defender[2], is_physical)

            if first_attacker[3] == 'a':
                hp_b -= damage
                hp_b = max(0, hp_b)
            else:
                hp_a -= damage
                hp_a = max(0, hp_a)

            # Log the attack
            effectiveness = ""
            if type_mult > 1:
                effectiveness = " (Super effective!)"
            elif type_mult < 1 and type_mult > 0:
                effectiveness = " (Not very effective...)"
            elif type_mult == 0:
                effectiveness = " (No effect!)"

            attack_type = "physical" if is_physical else "special"
            battle_log.append(f"⚔️ {first_attacker[0]} uses {attack_type} attack! {damage} damage{effectiveness}")

            if first_defender[3] == 'a':
                battle_log.append(f"💚 {name_a}: {hp_a}/{max_hp_a} HP remaining")
            else:
                battle_log.append(f"💚 {name_b}: {hp_b}/{max_hp_b} HP remaining")

        # Check if battle is over
        if hp_a <= 0 or hp_b <= 0:
            break

        # Second attack
        if (second_attacker[3] == 'a' and hp_a > 0) or (second_attacker[3] == 'b' and hp_b > 0):
            is_physical = second_attacker[1][1] > second_attacker[1][3]
            damage, type_mult = calculate_damage(second_attacker[1], second_defender[1], second_attacker[2], second_defender[2], is_physical)

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

            attack_type = "physical" if is_physical else "special"
            battle_log.append(f"⚔️ {second_attacker[0]} uses {attack_type} attack! {damage} damage{effectiveness}")

            if second_defender[3] == 'a':
                battle_log.append(f"💚 {name_a}: {hp_a}/{max_hp_a} HP remaining")
            else:
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
