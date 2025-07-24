// src/api.js
import { InputValidator, APISecurityUtils, clientRateLimit } from './security.js';

// Use environment variable for production deployment
// Remove trailing slash to prevent double slashes in URLs
const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

// Secure fetch wrapper
async function secureFetch(url, options = {}) {
  // Check rate limiting
  const endpoint = new URL(url).pathname;
  if (clientRateLimit.isRateLimited(endpoint)) {
    throw new Error('Too many requests. Please wait a moment before trying again.');
  }

  // Add security headers
  const secureOptions = APISecurityUtils.addSecurityHeaders(options);

  // Make request
  const response = await fetch(url, secureOptions);

  // Validate response
  APISecurityUtils.validateResponse(response);

  // Parse and sanitize response
  const data = await response.json();
  return APISecurityUtils.sanitizeResponseData(data);
}

export async function searchSimilar(stats) {
  // Validate input
  const validatedStats = InputValidator.validateStatsString(stats);

  // Make secure request
  return await secureFetch(`${API_BASE}/search_similar/?stats=${encodeURIComponent(validatedStats)}`);
}

export async function simulateBattle(statsA, statsB) {
  // Validate inputs
  const validatedStatsA = InputValidator.validateStatsString(statsA);
  const validatedStatsB = InputValidator.validateStatsString(statsB);

  // Make secure request
  return await secureFetch(`${API_BASE}/simulate_battle/?stats_a=${encodeURIComponent(validatedStatsA)}&stats_b=${encodeURIComponent(validatedStatsB)}`);
}

export async function searchByName(name, limit = 10) {
  // Validate inputs
  const validatedName = InputValidator.validatePokemonName(name);
  const validatedLimit = InputValidator.validateLimit(limit);

  // Make secure request
  return await secureFetch(`${API_BASE}/search_by_name/?name=${encodeURIComponent(validatedName)}&limit=${validatedLimit}`);
}

export async function getAllPokemon(limit = 1000) {
  // Validate input
  const validatedLimit = InputValidator.validateLimit(limit);

  // Make secure request
  return await secureFetch(`${API_BASE}/pokemon/?limit=${validatedLimit}`);
}

export async function getTopPokemon(criteria = 'power', limit = 10) {
  // Validate inputs (criteria validation happens on backend)
  const validatedLimit = InputValidator.validateLimit(limit);

  // Make secure request
  return await secureFetch(`${API_BASE}/pokemon/top/?criteria=${encodeURIComponent(criteria)}&limit=${validatedLimit}`);
}

export async function battleAdvanced(pokemonAName, pokemonBName) {
  // Validate inputs
  const validatedNameA = InputValidator.validatePokemonName(pokemonAName);
  const validatedNameB = InputValidator.validatePokemonName(pokemonBName);

  // Make secure request
  return await secureFetch(`${API_BASE}/battle_advanced/?pokemon_a_name=${encodeURIComponent(validatedNameA)}&pokemon_b_name=${encodeURIComponent(validatedNameB)}`);
}

export async function searchMoves(query, limit = 20) {
  // Validate inputs
  const validatedQuery = InputValidator.validateSearchQuery(query);
  const validatedLimit = InputValidator.validateLimit(limit);

  // Make secure request
  return await secureFetch(`${API_BASE}/search_moves/?query=${encodeURIComponent(validatedQuery)}&limit=${validatedLimit}`);
}

export async function getMoveDetails(moveName) {
  // Validate input
  const validatedName = InputValidator.validatePokemonName(moveName); // Reuse Pokemon name validation for move names

  // Make secure request
  return await secureFetch(`${API_BASE}/move_details/?name=${encodeURIComponent(validatedName)}`);
}
