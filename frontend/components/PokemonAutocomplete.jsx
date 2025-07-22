import React, { useState, useEffect, useRef } from 'react';
import { getAllPokemon } from '../api';

function PokemonAutocomplete({ 
  placeholder = "Enter Pokemon name...", 
  onSelect, 
  value = "", 
  onChange,
  disabled = false 
}) {
  const [allPokemon, setAllPokemon] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [activeSuggestion, setActiveSuggestion] = useState(-1);
  const [loading, setLoading] = useState(true);
  const inputRef = useRef(null);
  const suggestionsRef = useRef(null);

  // Load all Pokemon on component mount
  useEffect(() => {
    const loadPokemon = async () => {
      try {
        const data = await getAllPokemon(1000);
        setAllPokemon(data.results || []);
      } catch (error) {
        console.error('Error loading Pokemon:', error);
      } finally {
        setLoading(false);
      }
    };

    loadPokemon();
  }, []);

  // Fuzzy matching function with highlighting
  const fuzzyMatch = (searchTerm, pokemonName) => {
    const search = searchTerm.toLowerCase();
    const name = pokemonName.toLowerCase();

    // Exact match gets highest priority
    if (name === search) return { score: 100, highlighted: pokemonName };

    // Starts with gets high priority
    if (name.startsWith(search)) {
      const highlighted = pokemonName.substring(0, search.length) + pokemonName.substring(search.length);
      return { score: 90, highlighted };
    }

    // Contains gets medium priority
    if (name.includes(search)) {
      const index = name.indexOf(search);
      const highlighted = pokemonName.substring(0, index) +
                         pokemonName.substring(index, index + search.length) +
                         pokemonName.substring(index + search.length);
      return { score: 70, highlighted };
    }

    // Fuzzy character matching
    let searchIndex = 0;
    let score = 0;

    for (let i = 0; i < name.length && searchIndex < search.length; i++) {
      if (name[i] === search[searchIndex]) {
        score += 1;
        searchIndex++;
      }
    }

    // Return score based on how many characters matched
    if (searchIndex === search.length) {
      return {
        score: Math.max(0, 50 - (name.length - search.length)),
        highlighted: pokemonName
      };
    }

    return { score: 0, highlighted: pokemonName };
  };

  // Filter and sort suggestions
  const filterSuggestions = (input) => {
    if (!input.trim() || input.length < 1) {
      setSuggestions([]);
      return;
    }

    const matches = allPokemon
      .map(pokemon => {
        const matchResult = fuzzyMatch(input, pokemon.name);
        return {
          ...pokemon,
          score: matchResult.score,
          highlighted: matchResult.highlighted
        };
      })
      .filter(pokemon => pokemon.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 8); // Limit to 8 suggestions

    setSuggestions(matches);
  };

  // Handle input change
  const handleInputChange = (e) => {
    const inputValue = e.target.value;
    onChange && onChange(inputValue);
    
    filterSuggestions(inputValue);
    setShowSuggestions(true);
    setActiveSuggestion(-1);
  };

  // Handle suggestion selection
  const handleSuggestionClick = (pokemon) => {
    onChange && onChange(pokemon.name);
    onSelect && onSelect(pokemon);
    setShowSuggestions(false);
    setActiveSuggestion(-1);
  };

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveSuggestion(prev => 
          prev < suggestions.length - 1 ? prev + 1 : 0
        );
        break;
      
      case 'ArrowUp':
        e.preventDefault();
        setActiveSuggestion(prev => 
          prev > 0 ? prev - 1 : suggestions.length - 1
        );
        break;
      
      case 'Enter':
        e.preventDefault();
        if (activeSuggestion >= 0 && suggestions[activeSuggestion]) {
          handleSuggestionClick(suggestions[activeSuggestion]);
        }
        break;
      
      case 'Escape':
        setShowSuggestions(false);
        setActiveSuggestion(-1);
        break;
    }
  };

  // Handle input blur (with delay to allow clicking suggestions)
  const handleBlur = () => {
    setTimeout(() => {
      setShowSuggestions(false);
      setActiveSuggestion(-1);
    }, 150);
  };

  // Handle input focus
  const handleFocus = () => {
    if (value && suggestions.length > 0) {
      setShowSuggestions(true);
    }
  };

  return (
    <div className="pokemon-autocomplete">
      <input
        ref={inputRef}
        type="text"
        className="form-input"
        placeholder={loading ? "Loading Pokemon..." : placeholder}
        value={value}
        onChange={handleInputChange}
        onKeyDown={handleKeyDown}
        onBlur={handleBlur}
        onFocus={handleFocus}
        disabled={disabled || loading}
        autoComplete="off"
        style={{ width: '100%' }}
      />

      {showSuggestions && suggestions.length > 0 && (
        <div ref={suggestionsRef} className="pokemon-suggestions">
          {suggestions.map((pokemon, index) => (
            <div
              key={pokemon.id}
              onClick={() => handleSuggestionClick(pokemon)}
              className={`pokemon-suggestion ${index === activeSuggestion ? 'active' : ''}`}
              onMouseEnter={() => setActiveSuggestion(index)}
            >
              <img
                src={pokemon.metadata.sprite_url}
                alt={pokemon.name}
                className="pokemon-suggestion-sprite"
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
              <div className="pokemon-suggestion-info">
                <div className="pokemon-suggestion-name">
                  {pokemon.name}
                </div>
                <div className="pokemon-suggestion-details">
                  {pokemon.metadata.types.join(', ')} • Total: {
                    Object.values(pokemon.metadata.stats).reduce((a, b) => a + b, 0)
                  }
                </div>
              </div>
              <div className="pokemon-suggestion-id">
                #{pokemon.id}
              </div>
            </div>
          ))}
        </div>
      )}

      {showSuggestions && suggestions.length === 0 && value.trim() && !loading && (
        <div className="pokemon-suggestions">
          <div className="pokemon-no-results">
            No Pokemon found matching "{value}"
          </div>
        </div>
      )}
    </div>
  );
}

export default PokemonAutocomplete;
