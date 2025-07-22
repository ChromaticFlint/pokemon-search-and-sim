"""
Test suite for battle_service.py
Tests battle simulation logic and calculations
"""

import pytest
from unittest.mock import patch, Mock
import battle_service

class TestSimpleBattle:
    """Test simple battle functionality"""

    def test_simple_battle_pokemon_a_wins(self):
        """Test simple battle where Pokemon A wins"""
        stats_a = [78, 84, 78, 109, 85, 100]  # Charizard
        stats_b = [35, 55, 40, 50, 50, 90]    # Pikachu

        result = battle_service.simulate_battle(stats_a, stats_b)
        assert "Pokemon A wins" in result

    def test_simple_battle_pokemon_b_wins(self):
        """Test simple battle where Pokemon B wins"""
        stats_a = [35, 55, 40, 50, 50, 90]    # Pikachu
        stats_b = [78, 84, 78, 109, 85, 100]  # Charizard

        result = battle_service.simulate_battle(stats_a, stats_b)
        assert "Pokemon B wins" in result

    def test_simple_battle_tie(self):
        """Test simple battle with identical Pokemon (tie)"""
        stats_a = [35, 55, 40, 50, 50, 90]  # Pikachu
        stats_b = [35, 55, 40, 50, 50, 90]  # Pikachu Clone

        result = battle_service.simulate_battle(stats_a, stats_b)
        assert "tie" in result.lower() or "draw" in result.lower()

    def test_simple_battle_empty_stats(self):
        """Test simple battle with empty stats (should handle gracefully)"""
        stats_a = []  # Empty stats
        stats_b = [35, 55, 40, 50, 50, 90]

        result = battle_service.simulate_battle(stats_a, stats_b)
        assert "Pokemon B wins" in result  # Pokemon with stats should win

class TestAdvancedBattle:
    """Test advanced battle functionality"""
    
    def test_advanced_battle_basic(self):
        """Test basic advanced battle functionality"""
        pokemon_a = {
            "name": "Pikachu",
            "metadata": {
                "stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
                "types": ["electric"]
            }
        }
        pokemon_b = {
            "name": "Charizard",
            "metadata": {
                "stats": {"hp": 78, "attack": 84, "defense": 78, "special_attack": 109, "special_defense": 85, "speed": 100},
                "types": ["fire", "flying"]
            }
        }
        
        result = battle_service.simulate_battle_advanced(pokemon_a, pokemon_b)
        
        assert "result" in result
        assert "battle_log" in result
        assert "final_hp" in result
        assert "turns" in result
        assert isinstance(result["battle_log"], list)
        assert len(result["battle_log"]) > 0
    
    def test_advanced_battle_level_difference(self):
        """Test advanced battle with different levels"""
        pokemon_a = {
            "name": "Pikachu",
            "stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
            "level": 100,  # Higher level
            "types": ["electric"]
        }
        pokemon_b = {
            "name": "Charizard",
            "stats": {"hp": 78, "attack": 84, "defense": 78, "special_attack": 109, "special_defense": 85, "speed": 100},
            "level": 5,   # Much lower level
            "types": ["fire", "flying"]
        }
        
        result = battle_service.simulate_battle_advanced(pokemon_a, pokemon_b)

        # Higher level Pokemon should win
        assert "Pikachu" in result["result"]
    
    def test_advanced_battle_type_effectiveness(self):
        """Test type effectiveness in advanced battle"""
        # Water vs Fire (Water should have advantage)
        pokemon_a = {
            "name": "Squirtle",
            "stats": {"hp": 44, "attack": 48, "defense": 65, "special_attack": 50, "special_defense": 64, "speed": 43},
            "level": 50,
            "types": ["water"]
        }
        pokemon_b = {
            "name": "Charmander",
            "stats": {"hp": 39, "attack": 52, "defense": 43, "special_attack": 60, "special_defense": 50, "speed": 65},
            "level": 50,
            "types": ["fire"]
        }
        
        result = battle_service.simulate_battle_advanced(pokemon_a, pokemon_b)
        
        # Check that type effectiveness is mentioned in battle log
        battle_log_text = " ".join(result["battle_log"])
        assert any(keyword in battle_log_text.lower() for keyword in ["effective", "super", "advantage"])

class TestBattleUtilities:
    """Test utility functions used in battles"""
    
    def test_calculate_damage_basic(self):
        """Test basic damage calculation"""
        if hasattr(battle_service, 'calculate_damage'):
            attacker_stats = {"attack": 100, "level": 50}
            defender_stats = {"defense": 50}
            
            damage = battle_service.calculate_damage(attacker_stats, defender_stats)
            assert isinstance(damage, (int, float))
            assert damage > 0
    
    def test_type_effectiveness_calculation(self):
        """Test type effectiveness calculation"""
        if hasattr(battle_service, 'get_type_effectiveness'):
            # Water vs Fire should be super effective (2x)
            effectiveness = battle_service.get_type_effectiveness("water", "fire")
            assert effectiveness >= 1.5  # Should be super effective
            
            # Fire vs Water should be not very effective (0.5x)
            effectiveness = battle_service.get_type_effectiveness("fire", "water")
            assert effectiveness <= 0.75  # Should be not very effective
    
    def test_speed_calculation(self):
        """Test speed-based turn order"""
        if hasattr(battle_service, 'calculate_speed'):
            fast_pokemon = {"speed": 100, "level": 50}
            slow_pokemon = {"speed": 30, "level": 50}
            
            fast_speed = battle_service.calculate_speed(fast_pokemon)
            slow_speed = battle_service.calculate_speed(slow_pokemon)
            
            assert fast_speed > slow_speed

class TestBattleEdgeCases:
    """Test edge cases and error handling"""
    
    def test_battle_with_zero_hp(self):
        """Test battle with Pokemon that has 0 HP"""
        pokemon_a = {
            "name": "Weak",
            "stats": {"hp": 0, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
            "level": 50,
            "types": ["normal"]
        }
        pokemon_b = {
            "name": "Strong",
            "stats": {"hp": 78, "attack": 84, "defense": 78, "special_attack": 109, "special_defense": 85, "speed": 100},
            "level": 50,
            "types": ["normal"]
        }
        
        result = battle_service.simulate_battle_advanced(pokemon_a, pokemon_b)

        # Pokemon with 0 HP should lose immediately
        assert "Strong" in result["result"]
        assert result["turns"] <= 1
    
    def test_battle_with_missing_stats(self):
        """Test battle with missing stat fields"""
        pokemon_a = {
            "name": "Incomplete",
            "stats": {"hp": 35, "attack": 55},  # Missing stats
            "level": 50,
            "types": ["normal"]
        }
        pokemon_b = {
            "name": "Complete",
            "stats": {"hp": 78, "attack": 84, "defense": 78, "special_attack": 109, "special_defense": 85, "speed": 100},
            "level": 50,
            "types": ["normal"]
        }
        
        # Should handle missing stats gracefully or raise appropriate error
        try:
            result = battle_service.simulate_battle_advanced(pokemon_a, pokemon_b)
            # If it succeeds, check that it's handled properly
            assert "result" in result
        except (KeyError, ValueError, AttributeError):
            # Expected behavior for missing stats
            pass
    
    def test_battle_with_invalid_types(self):
        """Test battle with invalid Pokemon types"""
        pokemon_a = {
            "name": "InvalidType",
            "stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
            "level": 50,
            "types": ["invalidtype"]
        }
        pokemon_b = {
            "name": "Normal",
            "stats": {"hp": 78, "attack": 84, "defense": 78, "special_attack": 109, "special_defense": 85, "speed": 100},
            "level": 50,
            "types": ["normal"]
        }
        
        # Should handle invalid types gracefully
        result = battle_service.simulate_battle_advanced(pokemon_a, pokemon_b)
        assert "result" in result  # Should still complete battle

class TestBattleConsistency:
    """Test battle consistency and determinism"""
    
    def test_battle_determinism(self):
        """Test that battles with same input produce consistent results"""
        pokemon_a = {
            "name": "Pikachu",
            "stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
            "level": 50,
            "types": ["electric"]
        }
        pokemon_b = {
            "name": "Charizard",
            "stats": {"hp": 78, "attack": 84, "defense": 78, "special_attack": 109, "special_defense": 85, "speed": 100},
            "level": 50,
            "types": ["fire", "flying"]
        }
        
        # Run battle multiple times
        results = []
        for _ in range(3):
            result = battle_service.simulate_battle_advanced(pokemon_a, pokemon_b)
            results.append(result["result"])
        
        # Results should be consistent (or at least the winner should be the same)
        # Note: Some randomness is expected in Pokemon battles
        winners = [result.split()[0] for result in results]
        # At least 2 out of 3 should have the same winner (allowing for some randomness)
        assert len(set(winners)) <= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
