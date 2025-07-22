import requests
import time
import json
from vector_service import add_pokemon
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PokemonScraper:
    def __init__(self, base_url="https://pokeapi.co/api/v2"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pokemon-Search-Sim/1.0'
        })
    
    def get_pokemon_list(self, limit=151):
        """Get list of Pokemon (default: first 151 - original generation)"""
        try:
            url = f"{self.base_url}/pokemon?limit={limit}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()['results']
        except requests.RequestException as e:
            print(f"Error fetching Pokemon list: {e}")
            return []
    
    def get_pokemon_details(self, pokemon_url):
        """Get detailed Pokemon data including stats"""
        try:
            response = self.session.get(pokemon_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching Pokemon details from {pokemon_url}: {e}")
            return None
    
    def extract_pokemon_data(self, pokemon_data):
        """Extract relevant data from Pokemon API response"""
        if not pokemon_data:
            return None
        
        # Extract basic info
        pokemon_id = pokemon_data['id']
        name = pokemon_data['name'].title()
        
        # Extract base stats (HP, Attack, Defense, Special Attack, Special Defense, Speed)
        stats = {}
        for stat in pokemon_data['stats']:
            stat_name = stat['stat']['name']
            base_stat = stat['base_stat']
            stats[stat_name] = base_stat
        
        # Create stats array in consistent order
        stats_array = [
            stats.get('hp', 0),
            stats.get('attack', 0),
            stats.get('defense', 0),
            stats.get('special-attack', 0),
            stats.get('special-defense', 0),
            stats.get('speed', 0)
        ]
        
        # Extract additional metadata
        metadata = {
            'name': name,
            'height': pokemon_data.get('height', 0),
            'weight': pokemon_data.get('weight', 0),
            'types': [t['type']['name'] for t in pokemon_data.get('types', [])],
            'abilities': [a['ability']['name'] for a in pokemon_data.get('abilities', [])],
            'base_experience': pokemon_data.get('base_experience', 0),
            'sprite_url': pokemon_data.get('sprites', {}).get('front_default', ''),
            'stats': {
                'hp': stats.get('hp', 0),
                'attack': stats.get('attack', 0),
                'defense': stats.get('defense', 0),
                'special_attack': stats.get('special-attack', 0),
                'special_defense': stats.get('special-defense', 0),
                'speed': stats.get('speed', 0)
            }
        }
        
        return {
            'id': pokemon_id,
            'name': name,
            'stats': stats_array,
            'metadata': metadata
        }
    
    def scrape_and_store_pokemon(self, limit=151, delay=0.1):
        """Scrape Pokemon data and store in vector database"""
        print(f"Starting to scrape {limit} Pokemon...")
        
        # Get list of Pokemon
        pokemon_list = self.get_pokemon_list(limit)
        if not pokemon_list:
            print("Failed to get Pokemon list")
            return
        
        successful_imports = 0
        failed_imports = 0
        
        for i, pokemon in enumerate(pokemon_list, 1):
            try:
                print(f"Processing {i}/{len(pokemon_list)}: {pokemon['name']}")
                
                # Get detailed Pokemon data
                pokemon_data = self.get_pokemon_details(pokemon['url'])
                if not pokemon_data:
                    failed_imports += 1
                    continue
                
                # Extract and format data
                extracted_data = self.extract_pokemon_data(pokemon_data)
                if not extracted_data:
                    failed_imports += 1
                    continue
                
                # Store in vector database
                add_pokemon(
                    pokemon_id=extracted_data['id'],
                    name=extracted_data['name'],
                    stats=extracted_data['stats'],
                    metadata=extracted_data['metadata']
                )
                
                successful_imports += 1
                print(f"✓ Successfully imported {extracted_data['name']}")
                
                # Rate limiting to be respectful to the API
                time.sleep(delay)
                
            except Exception as e:
                print(f"✗ Error processing {pokemon['name']}: {e}")
                failed_imports += 1
                continue
        
        print(f"\nScraping completed!")
        print(f"Successfully imported: {successful_imports}")
        print(f"Failed imports: {failed_imports}")
        print(f"Total processed: {successful_imports + failed_imports}")

def main():
    """Main function to run the scraper"""
    scraper = PokemonScraper()
    
    # You can adjust these parameters:
    # limit: number of Pokemon to scrape (151 = original generation)
    # delay: seconds to wait between API calls (be respectful to the API)
    scraper.scrape_and_store_pokemon(limit=151, delay=0.1)

if __name__ == "__main__":
    main()
