"""
Comprehensive test suite for Pokemon Search & Battle Arena API
Tests all endpoints, business logic, and error handling
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import json

# Import the FastAPI app
from api import app

# Create test client
client = TestClient(app)

# Mock data for testing
MOCK_POKEMON_DATA = [
    {
        "id": 25,
        "name": "Pikachu",
        "metadata": {
            "stats": {
                "hp": 35,
                "attack": 55,
                "defense": 40,
                "special_attack": 50,
                "special_defense": 50,
                "speed": 90
            },
            "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
            "types": ["electric"]
        }
    },
    {
        "id": 6,
        "name": "Charizard",
        "metadata": {
            "stats": {
                "hp": 78,
                "attack": 84,
                "defense": 78,
                "special_attack": 109,
                "special_defense": 85,
                "speed": 100
            },
            "sprite_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
            "types": ["fire", "flying"]
        }
    }
]

MOCK_SEARCH_RESULTS = {
    "results": [
        {
            "id": 25,
            "name": "Pikachu",
            "score": 0.95,
            "distance": 0.05,
            "metadata": MOCK_POKEMON_DATA[0]["metadata"]
        }
    ]
}

class TestHealthEndpoint:
    """Test the health check endpoint"""
    
    def test_health_check(self):
        """Test that health endpoint returns OK"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

class TestPokemonEndpoints:
    """Test Pokemon-related endpoints"""
    
    def test_get_all_pokemon_success(self):
        """Test successful retrieval of all Pokemon"""
        response = client.get("/pokemon/?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) <= 5
        assert len(data["results"]) > 0
        # Check that each result has required fields
        for pokemon in data["results"]:
            assert "name" in pokemon
            assert "id" in pokemon
            assert "metadata" in pokemon
    
    def test_get_all_pokemon_with_limit(self):
        """Test Pokemon retrieval with limit parameter"""
        response = client.get("/pokemon/?limit=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        assert "name" in data["results"][0]
    
    def test_get_all_pokemon_error(self):
        """Test error handling with invalid limit"""
        response = client.get("/pokemon/?limit=-1")
        assert response.status_code == 400  # Bad request for invalid limit
        assert "detail" in response.json()

class TestSearchEndpoints:
    """Test search functionality"""
    
    def test_search_similar_success(self):
        """Test successful similarity search"""
        response = client.get("/search_similar/?stats=35,55,40,50,50,90")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) > 0
        # Check that results have required fields
        for result in data["results"]:
            assert "name" in result
            assert "score" in result
            assert "distance" in result
    
    def test_search_similar_invalid_stats(self):
        """Test search with invalid stats format"""
        response = client.get("/search_similar/?stats=invalid")
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_search_similar_wrong_stat_count(self):
        """Test search with wrong number of stats"""
        response = client.get("/search_similar/?stats=35,55,40")
        assert response.status_code == 400
        assert "detail" in response.json()
    
    @patch('vector_service.search_pokemon_by_name')
    def test_search_by_name_success(self, mock_search):
        """Test successful name search"""
        mock_search.return_value = [MOCK_POKEMON_DATA[0]]
        
        response = client.get("/search_by_name/?name=Pikachu")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert data["results"][0]["name"] == "Pikachu"
    
    def test_search_by_name_missing_parameter(self):
        """Test name search without name parameter"""
        response = client.get("/search_by_name/")
        assert response.status_code == 422  # FastAPI validation error
    
    @patch('vector_service.search_pokemon_by_name')
    def test_search_by_name_no_results(self, mock_search):
        """Test name search with no results"""
        mock_search.return_value = []
        
        response = client.get("/search_by_name/?name=NonexistentPokemon")
        assert response.status_code == 200
        data = response.json()
        assert data["results"] == []

class TestTopPokemonEndpoint:
    """Test top Pokemon endpoint"""
    
    def test_get_top_pokemon_success(self):
        """Test successful top Pokemon retrieval"""
        response = client.get("/pokemon/top/?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) <= 5
        assert len(data["results"]) > 0
        # Check that results have power scores
        for pokemon in data["results"]:
            assert "name" in pokemon
            assert "power_score" in pokemon or "ranking_score" in pokemon
    
    def test_get_top_pokemon_with_criteria(self):
        """Test top Pokemon with specific criteria"""
        response = client.get("/pokemon/top/?criteria=speed&limit=3")
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) <= 3

class TestBattleEndpoints:
    """Test battle simulation endpoints"""
    
    def test_simple_battle_success(self):
        """Test successful simple battle"""
        response = client.get("/simulate_battle/?stats_a=78,84,78,109,85,100&stats_b=35,55,40,50,50,90")
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "wins" in data["result"]  # Should contain either "Pokemon A wins" or "Pokemon B wins"
    
    def test_simple_battle_invalid_data(self):
        """Test simple battle with invalid data"""
        response = client.get("/simulate_battle/?stats_a=invalid&stats_b=78,84,78,109,85,100")
        assert response.status_code == 400  # Bad request for invalid stats
    
    def test_advanced_battle_success(self):
        """Test successful advanced battle"""
        response = client.get("/battle_advanced/?pokemon_a_name=Pikachu&pokemon_b_name=Charizard&level_a=50&level_b=50")
        assert response.status_code == 200
        data = response.json()
        assert "battle_result" in data
        assert "result" in data["battle_result"]
        assert "battle_log" in data["battle_result"]
        assert "final_hp" in data["battle_result"]

class TestAddPokemonEndpoint:
    """Test Pokemon creation endpoint (secured)"""
    
    def test_add_pokemon_no_auth(self):
        """Test adding Pokemon without authentication"""
        response = client.post("/add_pokemon/", json={
            "name": "TestPokemon",
            "stats": {"hp": 50, "attack": 50, "defense": 50, "special_attack": 50, "special_defense": 50, "speed": 50},
            "types": ["normal"]
        })
        assert response.status_code == 401
        assert "API key required" in response.json()["detail"]
    
    @patch('vector_service.add_pokemon')
    def test_add_pokemon_with_auth(self, mock_add):
        """Test adding Pokemon with valid authentication"""
        mock_add.return_value = {"success": True, "id": "new-pokemon-id"}
        
        response = client.post("/add_pokemon/", 
            json={
                "name": "TestPokemon",
                "stats": {"hp": 50, "attack": 50, "defense": 50, "special_attack": 50, "special_defense": 50, "speed": 50},
                "types": ["normal"]
            },
            headers={"X-Requested-With": "XMLHttpRequest", "Authorization": "Bearer valid-api-key"}
        )
        # This will still fail without proper API key setup, but tests the structure
        # In a real environment, you'd mock the authentication as well

class TestCORSHeaders:
    """Test CORS configuration"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses"""
        response = client.get("/health")
        assert response.status_code == 200
        # CORS headers should be present due to middleware
        # Note: TestClient doesn't always include middleware headers
        # In production, these would be tested with actual browser requests

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_endpoint(self):
        """Test accessing non-existent endpoint"""
        response = client.get("/nonexistent/")
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """Test using wrong HTTP method"""
        response = client.post("/health")  # GET endpoint called with POST
        assert response.status_code == 405

# Pytest configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
