#!/usr/bin/env python3
"""
Script to demonstrate the improvement in similarity algorithm
"""

import numpy as np
import requests

def old_similarity_algorithm(stats1, stats2):
    """Old algorithm using L2 normalization + cosine similarity"""
    v1 = np.array(stats1) / np.linalg.norm(stats1)
    v2 = np.array(stats2) / np.linalg.norm(stats2)
    
    # Cosine similarity
    cosine_sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return cosine_sim

def new_similarity_algorithm(stats1, stats2, max_distance=300):
    """New algorithm using Euclidean distance"""
    v1 = np.array(stats1)
    v2 = np.array(stats2)
    
    # Euclidean distance
    distance = np.linalg.norm(v1 - v2)
    
    # Convert to similarity percentage
    similarity = max(0, (max_distance - distance) / max_distance)
    return similarity, distance

def test_similarity_algorithms():
    """Test both algorithms with the problematic example"""
    
    # Moltres stats: [90,100,90,125,85,90]
    moltres_stats = [90, 100, 90, 125, 85, 90]
    
    # Psyduck stats: [50,52,48,65,50,55]
    psyduck_stats = [50, 52, 48, 65, 50, 55]
    
    # Some other Pokemon for comparison
    charizard_stats = [78, 84, 78, 109, 85, 100]  # Should be more similar to Moltres
    zapdos_stats = [90, 90, 85, 125, 90, 100]     # Should be very similar to Moltres
    
    print("=== SIMILARITY ALGORITHM COMPARISON ===\n")
    
    print("🔥 MOLTRES STATS: [90,100,90,125,85,90] (Total: 580)")
    print("🦆 PSYDUCK STATS: [50,52,48,65,50,55] (Total: 320)")
    print("🐉 CHARIZARD STATS: [78,84,78,109,85,100] (Total: 534)")
    print("⚡ ZAPDOS STATS: [90,90,85,125,90,100] (Total: 580)")
    print()
    
    # Test old algorithm
    print("--- OLD ALGORITHM (L2 Normalization + Cosine Similarity) ---")
    old_psyduck_sim = old_similarity_algorithm(moltres_stats, psyduck_stats)
    old_charizard_sim = old_similarity_algorithm(moltres_stats, charizard_stats)
    old_zapdos_sim = old_similarity_algorithm(moltres_stats, zapdos_stats)
    
    print(f"Moltres vs Psyduck:   {old_psyduck_sim:.4f} ({old_psyduck_sim*100:.1f}%)")
    print(f"Moltres vs Charizard: {old_charizard_sim:.4f} ({old_charizard_sim*100:.1f}%)")
    print(f"Moltres vs Zapdos:    {old_zapdos_sim:.4f} ({old_zapdos_sim*100:.1f}%)")
    print()
    
    # Test new algorithm
    print("--- NEW ALGORITHM (Euclidean Distance) ---")
    new_psyduck_sim, psyduck_dist = new_similarity_algorithm(moltres_stats, psyduck_stats)
    new_charizard_sim, charizard_dist = new_similarity_algorithm(moltres_stats, charizard_stats)
    new_zapdos_sim, zapdos_dist = new_similarity_algorithm(moltres_stats, zapdos_stats)
    
    print(f"Moltres vs Psyduck:   {new_psyduck_sim:.4f} ({new_psyduck_sim*100:.1f}%) [Distance: {psyduck_dist:.1f}]")
    print(f"Moltres vs Charizard: {new_charizard_sim:.4f} ({new_charizard_sim*100:.1f}%) [Distance: {charizard_dist:.1f}]")
    print(f"Moltres vs Zapdos:    {new_zapdos_sim:.4f} ({new_zapdos_sim*100:.1f}%) [Distance: {zapdos_dist:.1f}]")
    print()
    
    print("=== ANALYSIS ===")
    print("❌ OLD ALGORITHM PROBLEMS:")
    print(f"   • Psyduck shows {old_psyduck_sim*100:.1f}% similarity (way too high!)")
    print(f"   • Focuses on proportional relationships, not absolute differences")
    print(f"   • Normalized vectors lose magnitude information")
    print()
    
    print("✅ NEW ALGORITHM IMPROVEMENTS:")
    print(f"   • Psyduck shows {new_psyduck_sim*100:.1f}% similarity (much more realistic)")
    print(f"   • Zapdos shows {new_zapdos_sim*100:.1f}% similarity (correctly high)")
    print(f"   • Uses absolute stat differences, preserving magnitude")
    print(f"   • Euclidean distance provides intuitive similarity measure")
    print()
    
    print("🎯 RANKING CORRECTNESS:")
    print("   Old algorithm ranking: Psyduck > Charizard (WRONG!)")
    print("   New algorithm ranking: Zapdos > Charizard > Psyduck (CORRECT!)")

def test_api_endpoint():
    """Test the actual API endpoint"""
    print("\n=== TESTING API ENDPOINT ===")
    
    try:
        # Test Moltres stats
        response = requests.get("http://localhost:8000/search_similar/?stats=90,100,90,125,85,90&top_k=5")
        if response.status_code == 200:
            data = response.json()
            print("🔥 Searching for Moltres-like Pokemon:")
            for i, result in enumerate(data['results'], 1):
                name = result['name']
                score = result['score']
                distance = result.get('distance', 'N/A')
                print(f"   {i}. {name:<12} - {score*100:.1f}% similarity (distance: {distance})")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    test_similarity_algorithms()
    test_api_endpoint()
