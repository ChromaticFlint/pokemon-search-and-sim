from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from vector_service import search_similar, add_pokemon, search_pokemon_by_name, get_all_pokemon, get_top_pokemon
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
def advanced_battle_endpoint(pokemon_a_name: str, pokemon_b_name: str):
    """Advanced battle simulation with type effectiveness and input validation"""
    try:
        # Validate Pokemon names
        validated_name_a = SecurityValidator.validate_pokemon_name(pokemon_a_name)
        validated_name_b = SecurityValidator.validate_pokemon_name(pokemon_b_name)

        # Get Pokemon data
        pokemon_a_results = search_pokemon_by_name(validated_name_a, 1)
        pokemon_b_results = search_pokemon_by_name(validated_name_b, 1)

        if not pokemon_a_results:
            raise HTTPException(status_code=404, detail=f"Pokemon '{validated_name_a}' not found")
        if not pokemon_b_results:
            raise HTTPException(status_code=404, detail=f"Pokemon '{validated_name_b}' not found")

        pokemon_a = pokemon_a_results[0]
        pokemon_b = pokemon_b_results[0]

        # Simulate advanced battle
        battle_result = simulate_battle_advanced(pokemon_a, pokemon_b)

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
