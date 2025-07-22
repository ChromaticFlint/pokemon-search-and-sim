from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from vector_service import search_similar, add_pokemon, search_pokemon_by_name, get_all_pokemon, get_top_pokemon, search_moves, get_move_details
from battle_service import simulate_battle, simulate_battle_advanced
from security_fixes import SecurityValidator, RateLimiter, get_security_headers
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize rate limiter
rate_limiter = RateLimiter()

app = FastAPI(
    title="Pokemon Search and Sim API",
    description="Secure API for Pokemon search and battle simulation",
    version="1.0.0"
)

# Add CORS middleware with restricted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Specific frontend URLs only
    allow_credentials=False,  # Disable credentials for security
    allow_methods=["GET", "POST"],  # Only allow necessary methods
    allow_headers=["Content-Type", "Accept"],  # Restrict headers
)

# Security middleware
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    # Get client IP
    client_ip = request.client.host

    # Rate limiting
    if rate_limiter.is_rate_limited(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

    # Process request
    response = await call_next(request)

    # Add security headers
    for header, value in get_security_headers().items():
        response.headers[header] = value

    return response

@app.post("/add_pokemon/")
def add_pokemon_endpoint(id: int, name: str, stats: str):
    """Add a new Pokemon with input validation"""
    try:
        # Validate inputs
        validated_id = SecurityValidator.validate_pokemon_id(id)
        validated_name = SecurityValidator.validate_pokemon_name(name)
        validated_stats = SecurityValidator.validate_stats_string(stats)

        # Add Pokemon
        add_pokemon(validated_id, validated_name, validated_stats)

        logger.info(f"Added Pokemon: {validated_name} (ID: {validated_id})")
        return {"status": "added", "pokemon": validated_name}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding Pokemon: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/search_similar/")
def search_endpoint(stats: str):
    """Search for similar Pokemon with input validation"""
    try:
        # Validate stats input
        validated_stats = SecurityValidator.validate_stats_string(stats)

        # Perform search
        results = search_similar(validated_stats)

        return {"results": results}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in similarity search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/simulate_battle/")
def battle_endpoint(stats_a: str, stats_b: str):
    """Simulate battle between two Pokemon with input validation"""
    try:
        # Validate both stat inputs
        validated_stats_a = SecurityValidator.validate_stats_string(stats_a)
        validated_stats_b = SecurityValidator.validate_stats_string(stats_b)

        # Simulate battle
        result = simulate_battle(validated_stats_a, validated_stats_b)

        return {"result": result}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in battle simulation: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/battle_advanced/")
def advanced_battle_endpoint(pokemon_a_name: str, pokemon_b_name: str, level_a: int = 50, level_b: int = 50):
    """Enhanced battle simulation with movesets, status effects, and levels"""
    try:
        # Validate Pokemon names
        validated_name_a = SecurityValidator.validate_pokemon_name(pokemon_a_name)
        validated_name_b = SecurityValidator.validate_pokemon_name(pokemon_b_name)

        # Validate levels (1-100)
        if not (1 <= level_a <= 100) or not (1 <= level_b <= 100):
            raise HTTPException(status_code=400, detail="Pokemon levels must be between 1 and 100")

        # Get Pokemon data
        pokemon_a_results = search_pokemon_by_name(validated_name_a, 1)
        pokemon_b_results = search_pokemon_by_name(validated_name_b, 1)

        if not pokemon_a_results:
            raise HTTPException(status_code=404, detail=f"Pokemon '{validated_name_a}' not found")
        if not pokemon_b_results:
            raise HTTPException(status_code=404, detail=f"Pokemon '{validated_name_b}' not found")

        pokemon_a = pokemon_a_results[0]
        pokemon_b = pokemon_b_results[0]

        # Simulate enhanced battle
        battle_result = simulate_battle_advanced(pokemon_a, pokemon_b, level_a, level_b)

        return {
            "pokemon_a": pokemon_a['name'],
            "pokemon_b": pokemon_b['name'],
            "battle_result": battle_result
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in advanced battle: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/search_by_name/")
def search_by_name_endpoint(name: str, limit: int = 10):
    """Search Pokemon by name with input validation"""
    try:
        # Validate inputs
        validated_name = SecurityValidator.validate_pokemon_name(name)
        validated_limit = SecurityValidator.validate_limit(limit)

        # Perform search
        results = search_pokemon_by_name(validated_name, validated_limit)

        return {"results": results}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in name search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/pokemon/")
def get_all_pokemon_endpoint(limit: int = 1000):
    """Get all Pokemon with input validation"""
    try:
        # Validate limit
        validated_limit = SecurityValidator.validate_limit(limit)

        # Get Pokemon
        results = get_all_pokemon(validated_limit)

        return {"results": results}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting all Pokemon: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/pokemon/top/")
def get_top_pokemon_endpoint(criteria: str = "power", limit: int = 10):
    """
    Get top Pokemon by different criteria with input validation:
    - power: Weighted power score (default)
    - total: Total base stats
    - offensive: Offensive capability
    - defensive: Defensive capability
    - speed: Speed stat
    """
    try:
        # Validate inputs
        validated_criteria = SecurityValidator.validate_criteria(criteria)
        validated_limit = SecurityValidator.validate_limit(limit)

        # Get top Pokemon
        results = get_top_pokemon(validated_criteria, validated_limit)

        return {"results": results, "criteria": validated_criteria}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting top Pokemon: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/search_moves/")
def search_moves_endpoint(query: str, limit: int = 20):
    """Search for Pokemon moves using vector similarity"""
    try:
        # Validate query
        validated_query = SecurityValidator.validate_search_query(query)

        # Validate limit
        if not (1 <= limit <= 100):
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")

        # Search for moves
        results = search_moves(validated_query, limit)

        return {
            "query": validated_query,
            "results": results,
            "count": len(results)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in move search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/move_details/")
def move_details_endpoint(name: str):
    """Get detailed information about a specific move"""
    try:
        # Validate move name
        validated_name = SecurityValidator.validate_pokemon_name(name)  # Reuse Pokemon name validation

        # Get move details
        move_details = get_move_details(validated_name)

        if not move_details:
            raise HTTPException(status_code=404, detail=f"Move '{validated_name}' not found")

        return move_details
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting move details: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
