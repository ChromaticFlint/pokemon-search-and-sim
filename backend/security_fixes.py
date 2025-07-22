#!/usr/bin/env python3
"""
Security fixes and input validation for Pokemon Search and Sim application
"""

import re
from typing import List, Optional, Union
from fastapi import HTTPException

class SecurityValidator:
    """Input validation and sanitization utilities"""
    
    # Constants for validation
    MAX_POKEMON_NAME_LENGTH = 50
    MAX_STATS_VALUES = 6
    MIN_STAT_VALUE = 0
    MAX_STAT_VALUE = 999  # Pokemon stats typically don't exceed 255, but allow some buffer
    MAX_LIMIT_VALUE = 1000
    MAX_POKEMON_ID = 99999
    
    # Allowed criteria for rankings
    ALLOWED_CRITERIA = {"power", "total", "offensive", "defensive", "speed"}
    
    # Pokemon name pattern (letters, numbers, spaces, hyphens, apostrophes)
    POKEMON_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9\s\-'\.]+$")
    
    @staticmethod
    def validate_pokemon_name(name: str) -> str:
        """Validate and sanitize Pokemon name input"""
        if not name or not isinstance(name, str):
            raise HTTPException(status_code=400, detail="Pokemon name is required and must be a string")
        
        # Strip whitespace and convert to title case
        name = name.strip()
        
        if len(name) == 0:
            raise HTTPException(status_code=400, detail="Pokemon name cannot be empty")
        
        if len(name) > SecurityValidator.MAX_POKEMON_NAME_LENGTH:
            raise HTTPException(
                status_code=400, 
                detail=f"Pokemon name too long (max {SecurityValidator.MAX_POKEMON_NAME_LENGTH} characters)"
            )
        
        # Check for valid characters
        if not SecurityValidator.POKEMON_NAME_PATTERN.match(name):
            raise HTTPException(
                status_code=400, 
                detail="Pokemon name contains invalid characters. Only letters, numbers, spaces, hyphens, and apostrophes are allowed"
            )
        
        return name
    
    @staticmethod
    def validate_stats_string(stats_str: str) -> List[int]:
        """Validate and parse stats string"""
        if not stats_str or not isinstance(stats_str, str):
            raise HTTPException(status_code=400, detail="Stats string is required")
        
        # Remove whitespace
        stats_str = stats_str.strip()
        
        if not stats_str:
            raise HTTPException(status_code=400, detail="Stats string cannot be empty")
        
        # Split by comma and validate
        try:
            parts = stats_str.split(',')
            
            if len(parts) != SecurityValidator.MAX_STATS_VALUES:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Stats must contain exactly {SecurityValidator.MAX_STATS_VALUES} values (HP,Attack,Defense,Special Attack,Special Defense,Speed)"
                )
            
            stats = []
            for i, part in enumerate(parts):
                part = part.strip()
                
                # Check if it's a valid integer
                if not part.isdigit() and not (part.startswith('-') and part[1:].isdigit()):
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Stat value '{part}' is not a valid integer"
                    )
                
                stat_value = int(part)
                
                # Validate range
                if stat_value < SecurityValidator.MIN_STAT_VALUE or stat_value > SecurityValidator.MAX_STAT_VALUE:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Stat value {stat_value} is out of valid range ({SecurityValidator.MIN_STAT_VALUE}-{SecurityValidator.MAX_STAT_VALUE})"
                    )
                
                stats.append(stat_value)
            
            return stats
            
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid stats format: {str(e)}")
    
    @staticmethod
    def validate_pokemon_id(pokemon_id: Union[int, str]) -> int:
        """Validate Pokemon ID"""
        try:
            if isinstance(pokemon_id, str):
                pokemon_id = int(pokemon_id)
            
            if not isinstance(pokemon_id, int):
                raise ValueError("Pokemon ID must be an integer")
            
            if pokemon_id < 1 or pokemon_id > SecurityValidator.MAX_POKEMON_ID:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Pokemon ID must be between 1 and {SecurityValidator.MAX_POKEMON_ID}"
                )
            
            return pokemon_id
            
        except ValueError:
            raise HTTPException(status_code=400, detail="Pokemon ID must be a valid integer")
    
    @staticmethod
    def validate_limit(limit: Union[int, str]) -> int:
        """Validate limit parameter"""
        try:
            if isinstance(limit, str):
                limit = int(limit)
            
            if not isinstance(limit, int):
                raise ValueError("Limit must be an integer")
            
            if limit < 1:
                raise HTTPException(status_code=400, detail="Limit must be at least 1")
            
            if limit > SecurityValidator.MAX_LIMIT_VALUE:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Limit too large (max {SecurityValidator.MAX_LIMIT_VALUE})"
                )
            
            return limit
            
        except ValueError:
            raise HTTPException(status_code=400, detail="Limit must be a valid integer")
    
    @staticmethod
    def validate_criteria(criteria: str) -> str:
        """Validate ranking criteria"""
        if not criteria or not isinstance(criteria, str):
            raise HTTPException(status_code=400, detail="Criteria is required")
        
        criteria = criteria.lower().strip()
        
        if criteria not in SecurityValidator.ALLOWED_CRITERIA:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid criteria. Allowed values: {', '.join(SecurityValidator.ALLOWED_CRITERIA)}"
            )
        
        return criteria

    @staticmethod
    def validate_search_query(query: str) -> str:
        """Validate search query for moves"""
        if not query or not isinstance(query, str):
            raise HTTPException(status_code=400, detail="Search query is required and must be a string")

        # Strip whitespace
        query = query.strip()

        # Check minimum length
        if len(query) < 2:
            raise HTTPException(status_code=400, detail="Search query must be at least 2 characters long")

        # Check maximum length
        if len(query) > 200:
            raise HTTPException(status_code=400, detail="Search query must be less than 200 characters")

        # Allow letters, numbers, spaces, and common punctuation
        if not re.match(r"^[a-zA-Z0-9\s\-'\.!?]+$", query):
            raise HTTPException(status_code=400, detail="Search query contains invalid characters")

        return query

    @staticmethod
    def sanitize_error_message(message: str) -> str:
        """Sanitize error messages to prevent information disclosure"""
        # Remove potential file paths
        message = re.sub(r'[A-Za-z]:\\[^\\]+\\[^\\]+', '[PATH]', message)
        message = re.sub(r'/[^/]+/[^/]+', '[PATH]', message)
        
        # Remove potential SQL-like patterns
        message = re.sub(r'(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE)\s+', '[SQL]', message, flags=re.IGNORECASE)
        
        # Limit message length
        if len(message) > 200:
            message = message[:200] + "..."
        
        return message

# Rate limiting utilities
class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = {}
        self.max_requests_per_minute = 60
        self.max_requests_per_hour = 1000
    
    def is_rate_limited(self, client_ip: str) -> bool:
        """Check if client is rate limited"""
        import time
        current_time = time.time()
        
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Clean old requests (older than 1 hour)
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if current_time - req_time < 3600
        ]
        
        # Check hourly limit
        if len(self.requests[client_ip]) >= self.max_requests_per_hour:
            return True
        
        # Check per-minute limit
        recent_requests = [
            req_time for req_time in self.requests[client_ip] 
            if current_time - req_time < 60
        ]
        
        if len(recent_requests) >= self.max_requests_per_minute:
            return True
        
        # Add current request
        self.requests[client_ip].append(current_time)
        return False

# Security headers middleware
def get_security_headers():
    """Get security headers for responses"""
    return {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://pokeapi.co",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
