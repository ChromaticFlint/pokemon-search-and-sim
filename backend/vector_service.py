import os
import numpy as np
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct

# Load .env variables
load_dotenv()

# Retrieve from environment
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Connect to Qdrant Cloud
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Create collection only if it doesn't exist
try:
    client.get_collection("pokemon_stats")
    print("Collection 'pokemon_stats' already exists")
except Exception:
    print("Creating collection 'pokemon_stats'")
    client.create_collection(
        collection_name="pokemon_stats",
        vectors_config=VectorParams(size=6, distance="Euclid")
    )

def add_pokemon(pokemon_id, name, stats, metadata=None):
    # Store raw stats without normalization for better similarity matching
    vector = np.array(stats, dtype=float)

    # Create payload with name and optional metadata
    payload = {"name": name}
    if metadata:
        payload.update(metadata)

    point = PointStruct(
        id=pokemon_id,
        vector=vector.tolist(),
        payload=payload
    )
    client.upsert(collection_name="pokemon_stats", points=[point])

def search_similar(stats, top_k=5):
    # Use raw stats for search
    query_vector = np.array(stats, dtype=float)
    results = client.search(collection_name="pokemon_stats", query_vector=query_vector.tolist(), limit=top_k)

    # Convert Euclidean distance to similarity percentage
    formatted_results = []
    for res in results:
        # Euclidean distance - lower is better (0 = perfect match)
        distance = res.score

        # Convert to similarity percentage
        # For Pokemon stats, calculate a more intuitive similarity score
        # Perfect match = 100%, completely different = 0%
        max_reasonable_distance = 200  # Adjusted for better scaling
        similarity_percentage = max(0, (max_reasonable_distance - distance) / max_reasonable_distance)

        formatted_results.append({
            "name": res.payload["name"],
            "score": similarity_percentage,  # Now represents similarity (higher = more similar)
            "distance": distance,  # Raw distance for debugging
            "metadata": res.payload
        })

    return formatted_results

def search_pokemon_by_name(name, limit=10):
    """Search Pokemon by name using simple text matching"""
    # Get all Pokemon and filter by name on the client side
    all_results = client.scroll(
        collection_name="pokemon_stats",
        limit=1000,  # Get a large number to search through
        with_payload=True,
        with_vectors=False
    )

    # Filter results by name (case-insensitive partial matching)
    name_lower = name.lower()
    filtered_results = []

    for point in all_results[0]:
        pokemon_name = point.payload.get("name", "").lower()
        if name_lower in pokemon_name:
            filtered_results.append({
                "id": point.id,
                "name": point.payload["name"],
                "metadata": point.payload
            })
            if len(filtered_results) >= limit:
                break

    return filtered_results

def get_all_pokemon(limit=1000):
    """Get all Pokemon in the database"""
    results = client.scroll(
        collection_name="pokemon_stats",
        limit=limit,
        with_payload=True,
        with_vectors=False
    )

    return [{"id": point.id, "name": point.payload["name"], "metadata": point.payload} for point in results[0]]

def calculate_pokemon_power_score(pokemon):
    """Calculate a weighted power score for a Pokemon"""
    stats = pokemon['metadata']['stats']
    # Weight offensive stats higher as they're generally more valuable
    stat_weights = {
        'hp': 1.0,
        'attack': 1.2,
        'defense': 1.0,
        'special_attack': 1.2,
        'special_defense': 1.0,
        'speed': 1.1
    }

    score = (
        stats['hp'] * stat_weights['hp'] +
        stats['attack'] * stat_weights['attack'] +
        stats['defense'] * stat_weights['defense'] +
        stats['special_attack'] * stat_weights['special_attack'] +
        stats['special_defense'] * stat_weights['special_defense'] +
        stats['speed'] * stat_weights['speed']
    )
    return round(score, 2)

def get_top_pokemon(criteria='power', limit=10):
    """Get top Pokemon by different criteria"""
    all_pokemon = get_all_pokemon(1000)

    pokemon_with_scores = []

    for pokemon in all_pokemon:
        stats = pokemon['metadata']['stats']

        if criteria == 'power':
            score = calculate_pokemon_power_score(pokemon)
        elif criteria == 'total':
            score = sum(stats.values())
        elif criteria == 'offensive':
            score = stats['attack'] + stats['special_attack'] + (stats['speed'] * 0.5)
        elif criteria == 'defensive':
            score = stats['hp'] + stats['defense'] + stats['special_defense']
        elif criteria == 'speed':
            score = stats['speed']
        else:
            score = calculate_pokemon_power_score(pokemon)

        pokemon_with_scores.append({
            **pokemon,
            'power_score': calculate_pokemon_power_score(pokemon),
            'total_stats': sum(stats.values()),
            'ranking_score': score
        })

    # Sort by ranking score (descending)
    pokemon_with_scores.sort(key=lambda x: x['ranking_score'], reverse=True)

    return pokemon_with_scores[:limit]

def search_moves(query, limit=20):
    """Search for Pokemon moves using vector similarity"""
    try:
        # For now, return mock data since we haven't populated move data yet
        # This will be replaced with actual vector search once we populate the database

        from battle_service import MOVE_DATABASE

        # Simple text matching for now - will be replaced with vector search
        query_lower = query.lower()
        matching_moves = []

        for move_key, move_data in MOVE_DATABASE.items():
            score = 0
            move_text = f"{move_data['name']} {move_data['type']} {move_data['category']}".lower()

            # Simple keyword matching
            query_words = query_lower.split()
            for word in query_words:
                if word in move_text:
                    score += 1
                if word in move_data['name'].lower():
                    score += 2  # Higher score for name matches

            # Add power-based matching
            if 'powerful' in query_lower or 'strong' in query_lower or 'high damage' in query_lower:
                if move_data['power'] and move_data['power'] >= 100:
                    score += 3

            # Add status effect matching
            if move_data.get('effect'):
                if move_data['effect'] in query_lower:
                    score += 2

            # Add accuracy matching
            if 'accurate' in query_lower and move_data['accuracy'] >= 95:
                score += 1
            if 'miss' in query_lower or 'unreliable' in query_lower and move_data['accuracy'] < 90:
                score += 1

            if score > 0:
                matching_moves.append({
                    'name': move_data['name'],
                    'type': move_data['type'],
                    'category': move_data['category'],
                    'power': move_data['power'],
                    'accuracy': move_data['accuracy'],
                    'effect': move_data.get('effect'),
                    'similarity': min(score / 5.0, 1.0),  # Normalize to 0-1
                    'description': f"A {move_data['category']} {move_data['type']}-type move with {move_data['power'] or 'variable'} power."
                })

        # Sort by similarity score and limit results
        matching_moves.sort(key=lambda x: x['similarity'], reverse=True)
        return matching_moves[:limit]

    except Exception as e:
        print(f"Error searching moves: {e}")
        return []

def get_move_details(move_name):
    """Get detailed information about a specific move"""
    try:
        from battle_service import MOVE_DATABASE

        # Find move in database (case-insensitive)
        move_key = None
        for key, move_data in MOVE_DATABASE.items():
            if move_data['name'].lower() == move_name.lower():
                move_key = key
                break

        if not move_key:
            return None

        move_data = MOVE_DATABASE[move_key]

        # Get Pokemon that can learn this move (mock data for now)
        learners = [
            {'name': 'Pikachu', 'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png'},
            {'name': 'Raichu', 'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/26.png'},
            {'name': 'Magnezone', 'sprite_url': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/462.png'}
        ]

        return {
            'name': move_data['name'],
            'type': move_data['type'],
            'category': move_data['category'],
            'power': move_data['power'],
            'accuracy': move_data['accuracy'],
            'pp': 15,  # Mock PP data
            'effect': move_data.get('effect'),
            'effect_chance': move_data.get('effect_chance', 0),
            'crit_ratio': move_data.get('crit_ratio', 1),
            'description': f"A {move_data['category']} {move_data['type']}-type move. " +
                          (f"Has a {move_data.get('effect_chance', 0)}% chance to cause {move_data.get('effect', 'no effect')}." if move_data.get('effect') else ""),
            'learners': learners
        }

    except Exception as e:
        print(f"Error getting move details: {e}")
        return None
