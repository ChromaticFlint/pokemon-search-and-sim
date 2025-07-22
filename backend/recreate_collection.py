#!/usr/bin/env python3
"""
Script to recreate the Pokemon collection with improved similarity algorithm
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

# Load environment variables
load_dotenv()

def recreate_collection():
    """Recreate the collection with Euclidean distance"""
    # Initialize client
    client = QdrantClient(
        url=os.getenv("QDRANT_URL", "http://localhost:6333"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    collection_name = "pokemon_stats"
    
    try:
        # Delete existing collection
        print(f"Deleting existing collection '{collection_name}'...")
        client.delete_collection(collection_name)
        print("✓ Collection deleted")
    except Exception as e:
        print(f"Collection might not exist: {e}")
    
    # Create new collection with Euclidean distance
    print(f"Creating new collection '{collection_name}' with Euclidean distance...")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=6, distance="Euclid")
    )
    print("✓ Collection created with Euclidean distance")
    
    return True

if __name__ == "__main__":
    if recreate_collection():
        print("\n✅ Collection recreated successfully!")
        print("Now run: python pokemon_scraper.py")
        print("This will re-import all Pokemon with the new similarity algorithm.")
    else:
        print("\n❌ Failed to recreate collection")
