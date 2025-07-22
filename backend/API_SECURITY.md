# Pokemon API Security Documentation

## 🔒 API Key Authentication

### Overview
The Pokemon Search and Sim API implements API key authentication for write operations to protect database integrity while maintaining public access for read operations.

### Security Model

#### **Public Endpoints (No Authentication Required)**
- `GET /search_similar/` - Search for similar Pokemon
- `GET /search_by_name/` - Search Pokemon by name  
- `GET /pokemon/` - Get all Pokemon
- `GET /pokemon/top/` - Get top Pokemon rankings
- `GET /simulate_battle/` - Simple battle simulation
- `GET /battle_advanced/` - Advanced battle simulation
- `GET /search_moves/` - Search Pokemon moves
- `GET /move_details/` - Get move details

#### **Protected Endpoints (API Key Required)**
- `POST /add_pokemon/` - Add new Pokemon to database

### API Key Authentication

#### **Required Header**
```
X-API-Key: <your-api-key>
```

#### **API Key Source**
The API uses the same key as the Qdrant database connection (`QDRANT_API_KEY` environment variable).

#### **Example Usage**

**✅ Successful Request:**
```bash
curl -X POST "http://localhost:8000/add_pokemon/?id=999&name=TestPokemon&stats=50,50,50,50,50,50" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-actual-api-key"
```

**Response:**
```json
{
  "status": "added",
  "pokemon": "TestPokemon", 
  "message": "Pokemon successfully added to database"
}
```

**❌ Missing API Key:**
```bash
curl -X POST "http://localhost:8000/add_pokemon/?id=999&name=TestPokemon&stats=50,50,50,50,50,50" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "detail": "API key required for write operations. Include 'X-API-Key' header."
}
```

**❌ Invalid API Key:**
```bash
curl -X POST "http://localhost:8000/add_pokemon/?id=999&name=TestPokemon&stats=50,50,50,50,50,50" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: invalid-key"
```

**Response:**
```json
{
  "detail": "Invalid API key. Access denied."
}
```

### Security Features

#### **Input Validation**
All endpoints include comprehensive input validation:
- Pokemon ID validation (positive integers)
- Pokemon name sanitization (alphanumeric + spaces/hyphens)
- Stats string validation (6 comma-separated numbers)
- SQL injection prevention
- XSS protection

#### **Rate Limiting**
- Per-IP rate limiting to prevent abuse
- Configurable limits for different endpoint types
- Automatic blocking of excessive requests

#### **Security Headers**
All responses include security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security`
- `Content-Security-Policy`

#### **CORS Configuration**
- Restricted to specific frontend origins (`http://localhost:3000`, `http://127.0.0.1:3000`)
- Limited HTTP methods (GET, POST only)
- Controlled headers (includes X-API-Key for write operations, X-Requested-With for frontend security)

### Environment Configuration

#### **Required Environment Variables**
```bash
# .env file
QDRANT_URL=https://your-qdrant-instance.cloud.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key
```

#### **Security Best Practices**
1. **Keep API Key Secret**: Never commit API keys to version control
2. **Use HTTPS**: Always use HTTPS in production
3. **Rotate Keys**: Regularly rotate API keys
4. **Monitor Access**: Log and monitor API key usage
5. **Principle of Least Privilege**: Only grant write access when necessary

### Error Handling

#### **Authentication Errors**
- `401 Unauthorized`: Missing API key
- `403 Forbidden`: Invalid API key

#### **Validation Errors**
- `400 Bad Request`: Invalid input parameters
- `422 Unprocessable Entity`: Malformed data

#### **Rate Limiting**
- `429 Too Many Requests`: Rate limit exceeded

### Logging and Monitoring

#### **Security Events Logged**
- API key authentication attempts (success/failure)
- Rate limiting violations
- Input validation failures
- Successful Pokemon additions

#### **Log Format**
```
INFO: Authenticated user added Pokemon: TestPokemon (ID: 999)
WARNING: API key missing for write operation
WARNING: Invalid API key attempted for write operation
```

### Implementation Details

#### **Authentication Function**
```python
async def verify_api_key(x_api_key: str = Header(None)):
    """Verify API key for write operations"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    if x_api_key != QDRANT_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return True
```

#### **Protected Endpoint Example**
```python
@app.post("/add_pokemon/")
def add_pokemon_endpoint(
    id: int, 
    name: str, 
    stats: str, 
    authenticated: bool = Depends(verify_api_key)
):
    # Endpoint implementation
```

### Testing

#### **Security Test Cases**
1. ✅ Add Pokemon with valid API key
2. ✅ Reject request without API key (401)
3. ✅ Reject request with invalid API key (403)
4. ✅ Allow read operations without authentication
5. ✅ Validate all input parameters
6. ✅ Respect rate limiting

This security implementation ensures that:
- **Database integrity** is protected from unauthorized modifications
- **Public access** is maintained for search and battle features
- **API key management** follows security best practices
- **Comprehensive logging** enables security monitoring
