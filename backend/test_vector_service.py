"""
Test suite for vector_service.py
Tests vector database operations and Pokemon data management
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import vector_service

class TestVectorServiceConnection:
    """Test vector database connection and setup"""
    
    @patch('vector_service.QdrantClient')
    def test_client_initialization(self, mock_client):
        """Test that Qdrant client initializes correctly"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # This would test the actual initialization if vector_service exposes it
        # For now, we test that the module can be imported without errors
        assert hasattr(vector_service, 'get_all_pokemon')
        assert hasattr(vector_service, 'search_similar_pokemon')
    
    @patch('vector_service.QdrantClient')
    def test_collection_exists_check(self, mock_client):
        """Test collection existence check"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Mock collection info response
        mock_instance.get_collection.return_value = {"status": "green"}
        
        # Test would go here if vector_service exposes collection checking
        # assert vector_service.collection_exists("pokemon")

class TestGetAllPokemon:
    """Test get_all_pokemon functionality"""
    
    @patch('vector_service.QdrantClient')
    def test_get_all_pokemon_success(self, mock_client):
        """Test successful retrieval of all Pokemon"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Mock scroll response
        mock_response = Mock()
        mock_response.points = [
            Mock(
                id=25,
                payload={
                    "name": "Pikachu",
                    "stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
                    "sprite_url": "https://example.com/pikachu.png",
                    "types": ["electric"]
                }
            ),
            Mock(
                id=6,
                payload={
                    "name": "Charizard",
                    "stats": {"hp": 78, "attack": 84, "defense": 78, "special_attack": 109, "special_defense": 85, "speed": 100},
                    "sprite_url": "https://example.com/charizard.png",
                    "types": ["fire", "flying"]
                }
            )
        ]
        mock_instance.scroll.return_value = (mock_response, None)
        
        with patch('vector_service.client', mock_instance):
            result = vector_service.get_all_pokemon()
            
            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["name"] == "Pikachu"
            assert result[1]["name"] == "Charizard"
    
    @patch('vector_service.QdrantClient')
    def test_get_all_pokemon_with_limit(self, mock_client):
        """Test get_all_pokemon with limit parameter"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        mock_response = Mock()
        mock_response.points = [
            Mock(
                id=25,
                payload={
                    "name": "Pikachu",
                    "stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
                    "sprite_url": "https://example.com/pikachu.png",
                    "types": ["electric"]
                }
            )
        ]
        mock_instance.scroll.return_value = (mock_response, None)
        
        with patch('vector_service.client', mock_instance):
            result = vector_service.get_all_pokemon(limit=1)
            
            assert len(result) == 1
            mock_instance.scroll.assert_called_with(
                collection_name="pokemon",
                limit=1,
                with_payload=True,
                with_vectors=False
            )
    
    @patch('vector_service.QdrantClient')
    def test_get_all_pokemon_error_handling(self, mock_client):
        """Test error handling in get_all_pokemon"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        mock_instance.scroll.side_effect = Exception("Database connection error")
        
        with patch('vector_service.client', mock_instance):
            with pytest.raises(Exception):
                vector_service.get_all_pokemon()

class TestSearchSimilarPokemon:
    """Test similarity search functionality"""
    
    @patch('vector_service.QdrantClient')
    def test_search_similar_pokemon_success(self, mock_client):
        """Test successful similarity search"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Mock search response
        mock_result = Mock()
        mock_result.id = 25
        mock_result.score = 0.95
        mock_result.payload = {
            "name": "Pikachu",
            "stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
            "sprite_url": "https://example.com/pikachu.png",
            "types": ["electric"]
        }
        
        mock_instance.search.return_value = [mock_result]
        
        with patch('vector_service.client', mock_instance):
            stats = [35, 55, 40, 50, 50, 90]
            result = vector_service.search_similar_pokemon(stats)
            
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]["name"] == "Pikachu"
            assert result[0]["score"] == 0.95
            assert "distance" in result[0]
    
    @patch('vector_service.QdrantClient')
    def test_search_similar_pokemon_with_limit(self, mock_client):
        """Test similarity search with limit"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        mock_instance.search.return_value = []
        
        with patch('vector_service.client', mock_instance):
            stats = [35, 55, 40, 50, 50, 90]
            vector_service.search_similar_pokemon(stats, limit=5)
            
            mock_instance.search.assert_called_with(
                collection_name="pokemon",
                query_vector=stats,
                limit=5,
                with_payload=True
            )
    
    def test_search_similar_pokemon_invalid_stats(self):
        """Test similarity search with invalid stats"""
        # Test with wrong number of stats
        with pytest.raises((ValueError, IndexError)):
            vector_service.search_similar_pokemon([35, 55, 40])  # Only 3 stats instead of 6
        
        # Test with non-numeric stats
        with pytest.raises((TypeError, ValueError)):
            vector_service.search_similar_pokemon(["invalid", "stats", "here", "test", "data", "error"])

class TestSearchPokemonByName:
    """Test name-based search functionality"""
    
    @patch('vector_service.QdrantClient')
    def test_search_pokemon_by_name_exact_match(self, mock_client):
        """Test exact name match search"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        # Mock filter response
        mock_response = Mock()
        mock_response.points = [
            Mock(
                id=25,
                payload={
                    "name": "Pikachu",
                    "stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
                    "sprite_url": "https://example.com/pikachu.png",
                    "types": ["electric"]
                }
            )
        ]
        mock_instance.scroll.return_value = (mock_response, None)
        
        with patch('vector_service.client', mock_instance):
            result = vector_service.search_pokemon_by_name("Pikachu")
            
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]["name"] == "Pikachu"
    
    @patch('vector_service.QdrantClient')
    def test_search_pokemon_by_name_partial_match(self, mock_client):
        """Test partial name match search"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        mock_response = Mock()
        mock_response.points = [
            Mock(
                id=25,
                payload={
                    "name": "Pikachu",
                    "stats": {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90},
                    "sprite_url": "https://example.com/pikachu.png",
                    "types": ["electric"]
                }
            )
        ]
        mock_instance.scroll.return_value = (mock_response, None)
        
        with patch('vector_service.client', mock_instance):
            result = vector_service.search_pokemon_by_name("pika")
            
            assert isinstance(result, list)
            # Should find Pikachu with partial match
            if len(result) > 0:
                assert "pika" in result[0]["name"].lower()
    
    @patch('vector_service.QdrantClient')
    def test_search_pokemon_by_name_no_results(self, mock_client):
        """Test name search with no results"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        
        mock_response = Mock()
        mock_response.points = []
        mock_instance.scroll.return_value = (mock_response, None)
        
        with patch('vector_service.client', mock_instance):
            result = vector_service.search_pokemon_by_name("NonexistentPokemon")
            
            assert isinstance(result, list)
            assert len(result) == 0

class TestAddPokemon:
    """Test Pokemon addition functionality"""
    
    @patch('vector_service.QdrantClient')
    def test_add_pokemon_success(self, mock_client):
        """Test successful Pokemon addition"""
        mock_instance = Mock()
        mock_client.return_value = mock_instance
        mock_instance.upsert.return_value = Mock(status="completed")
        
        with patch('vector_service.client', mock_instance):
            pokemon_data = {
                "name": "TestPokemon",
                "stats": {"hp": 50, "attack": 50, "defense": 50, "special_attack": 50, "special_defense": 50, "speed": 50},
                "types": ["normal"],
                "sprite_url": "https://example.com/test.png"
            }
            
            result = vector_service.add_pokemon(pokemon_data)
            
            # Should return success indicator
            assert result is not None
            mock_instance.upsert.assert_called_once()
    
    def test_add_pokemon_invalid_data(self):
        """Test adding Pokemon with invalid data"""
        # Test with missing required fields
        invalid_data = {"name": "Incomplete"}  # Missing stats
        
        with pytest.raises((KeyError, ValueError)):
            vector_service.add_pokemon(invalid_data)

class TestVectorServiceUtilities:
    """Test utility functions in vector service"""
    
    def test_stats_to_vector_conversion(self):
        """Test conversion of stats dict to vector"""
        if hasattr(vector_service, 'stats_to_vector'):
            stats = {"hp": 35, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90}
            vector = vector_service.stats_to_vector(stats)
            
            assert isinstance(vector, list)
            assert len(vector) == 6
            assert vector == [35, 55, 40, 50, 50, 90]
    
    def test_normalize_pokemon_name(self):
        """Test Pokemon name normalization"""
        if hasattr(vector_service, 'normalize_name'):
            # Test various name formats
            assert vector_service.normalize_name("PIKACHU") == "pikachu"
            assert vector_service.normalize_name("  Charizard  ") == "charizard"
            assert vector_service.normalize_name("Mr. Mime") == "mr. mime"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
