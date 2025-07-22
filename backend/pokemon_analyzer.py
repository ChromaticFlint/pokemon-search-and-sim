import requests
import json
import numpy as np
from vector_service import get_all_pokemon

class PokemonAnalyzer:
    def __init__(self):
        self.pokemon_data = []
        self.stat_weights = {
            'hp': 1.0,
            'attack': 1.2,
            'defense': 1.0,
            'special_attack': 1.2,
            'special_defense': 1.0,
            'speed': 1.1
        }
    
    def load_pokemon_data(self):
        """Load all Pokemon data from the vector database"""
        try:
            results = get_all_pokemon(1000)
            self.pokemon_data = results
            print(f"Loaded {len(self.pokemon_data)} Pokemon for analysis")
            return True
        except Exception as e:
            print(f"Error loading Pokemon data: {e}")
            return False
    
    def calculate_base_stat_total(self, pokemon):
        """Calculate the basic sum of all base stats"""
        stats = pokemon['metadata']['stats']
        return (stats['hp'] + stats['attack'] + stats['defense'] + 
                stats['special_attack'] + stats['special_defense'] + stats['speed'])
    
    def calculate_weighted_power_score(self, pokemon):
        """Calculate a weighted power score based on stat importance"""
        stats = pokemon['metadata']['stats']
        score = (
            stats['hp'] * self.stat_weights['hp'] +
            stats['attack'] * self.stat_weights['attack'] +
            stats['defense'] * self.stat_weights['defense'] +
            stats['special_attack'] * self.stat_weights['special_attack'] +
            stats['special_defense'] * self.stat_weights['special_defense'] +
            stats['speed'] * self.stat_weights['speed']
        )
        return round(score, 2)
    
    def calculate_offensive_rating(self, pokemon):
        """Calculate offensive capability (Attack + Special Attack + Speed)"""
        stats = pokemon['metadata']['stats']
        return stats['attack'] + stats['special_attack'] + (stats['speed'] * 0.5)
    
    def calculate_defensive_rating(self, pokemon):
        """Calculate defensive capability (HP + Defense + Special Defense)"""
        stats = pokemon['metadata']['stats']
        return stats['hp'] + stats['defense'] + stats['special_defense']
    
    def calculate_balanced_rating(self, pokemon):
        """Calculate how balanced a Pokemon's stats are (lower variance = more balanced)"""
        stats = pokemon['metadata']['stats']
        stat_values = [stats['hp'], stats['attack'], stats['defense'], 
                      stats['special_attack'], stats['special_defense'], stats['speed']]
        return -np.var(stat_values)  # Negative variance (higher is more balanced)
    
    def analyze_stat_distributions(self):
        """Analyze the distribution of each stat across all Pokemon"""
        if not self.pokemon_data:
            print("No Pokemon data loaded")
            return
        
        stats_data = {
            'hp': [],
            'attack': [],
            'defense': [],
            'special_attack': [],
            'special_defense': [],
            'speed': [],
            'total': []
        }
        
        for pokemon in self.pokemon_data:
            stats = pokemon['metadata']['stats']
            stats_data['hp'].append(stats['hp'])
            stats_data['attack'].append(stats['attack'])
            stats_data['defense'].append(stats['defense'])
            stats_data['special_attack'].append(stats['special_attack'])
            stats_data['special_defense'].append(stats['special_defense'])
            stats_data['speed'].append(stats['speed'])
            stats_data['total'].append(self.calculate_base_stat_total(pokemon))
        
        print("\n=== POKEMON STAT ANALYSIS ===")
        for stat_name, values in stats_data.items():
            print(f"\n{stat_name.upper().replace('_', ' ')}:")
            print(f"  Min: {min(values)}")
            print(f"  Max: {max(values)}")
            print(f"  Average: {np.mean(values):.1f}")
            print(f"  Median: {np.median(values):.1f}")
            print(f"  Std Dev: {np.std(values):.1f}")
    
    def get_top_pokemon_by_criteria(self, criteria='total', limit=10):
        """Get top Pokemon by different criteria"""
        if not self.pokemon_data:
            return []
        
        pokemon_with_scores = []
        
        for pokemon in self.pokemon_data:
            if criteria == 'total':
                score = self.calculate_base_stat_total(pokemon)
            elif criteria == 'weighted':
                score = self.calculate_weighted_power_score(pokemon)
            elif criteria == 'offensive':
                score = self.calculate_offensive_rating(pokemon)
            elif criteria == 'defensive':
                score = self.calculate_defensive_rating(pokemon)
            elif criteria == 'balanced':
                score = self.calculate_balanced_rating(pokemon)
            else:
                score = self.calculate_base_stat_total(pokemon)
            
            pokemon_with_scores.append({
                'pokemon': pokemon,
                'score': score,
                'total_stats': self.calculate_base_stat_total(pokemon)
            })
        
        # Sort by score (descending)
        pokemon_with_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return pokemon_with_scores[:limit]
    
    def print_rankings(self):
        """Print various Pokemon rankings"""
        if not self.pokemon_data:
            print("No Pokemon data loaded")
            return
        
        rankings = {
            'Highest Base Stat Total': self.get_top_pokemon_by_criteria('total', 10),
            'Highest Weighted Power Score': self.get_top_pokemon_by_criteria('weighted', 10),
            'Best Offensive Pokemon': self.get_top_pokemon_by_criteria('offensive', 10),
            'Best Defensive Pokemon': self.get_top_pokemon_by_criteria('defensive', 10),
            'Most Balanced Pokemon': self.get_top_pokemon_by_criteria('balanced', 10)
        }
        
        for category, top_pokemon in rankings.items():
            print(f"\n=== {category.upper()} ===")
            for i, entry in enumerate(top_pokemon, 1):
                pokemon = entry['pokemon']
                score = entry['score']
                total = entry['total_stats']
                stats = pokemon['metadata']['stats']
                
                print(f"{i:2d}. {pokemon['name']:<12} | Score: {score:6.1f} | Total: {total:3d} | "
                      f"HP:{stats['hp']:3d} ATK:{stats['attack']:3d} DEF:{stats['defense']:3d} "
                      f"SPA:{stats['special_attack']:3d} SPD:{stats['special_defense']:3d} SPE:{stats['speed']:3d}")
    
    def get_featured_pokemon(self, count=6):
        """Get the best Pokemon for featuring on the home page"""
        # Use weighted power score for featured Pokemon
        top_pokemon = self.get_top_pokemon_by_criteria('weighted', count)
        return [entry['pokemon'] for entry in top_pokemon]

def main():
    analyzer = PokemonAnalyzer()
    
    if not analyzer.load_pokemon_data():
        return
    
    # Analyze stat distributions
    analyzer.analyze_stat_distributions()
    
    # Print rankings
    analyzer.print_rankings()
    
    # Get featured Pokemon
    featured = analyzer.get_featured_pokemon(6)
    print(f"\n=== RECOMMENDED FEATURED POKEMON ===")
    for i, pokemon in enumerate(featured, 1):
        stats = pokemon['metadata']['stats']
        total = analyzer.calculate_base_stat_total(pokemon)
        weighted = analyzer.calculate_weighted_power_score(pokemon)
        print(f"{i}. {pokemon['name']} - Total: {total}, Weighted: {weighted}")

if __name__ == "__main__":
    main()
