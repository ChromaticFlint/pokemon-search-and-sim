import { useState } from 'react';
import PokemonAutocomplete from './PokemonAutocomplete';
import PokemonRadarChart from './PokemonRadarChart';

function Search() {
  const [searchType, setSearchType] = useState('name');
  const [statsInput, setStatsInput] = useState('');
  const [nameInput, setNameInput] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [viewMode, setViewMode] = useState('list'); // 'list' or 'radar'
  const [selectedLevel, setSelectedLevel] = useState(50);
  const [radarMode, setRadarMode] = useState('comparison'); // 'comparison', 'growth', 'level-only'

  const handleStatsSearch = async () => {
    if (!statsInput.trim()) return;

    setLoading(true);
    try {
      // Direct API call for stats search
      // This bypasses frontend validation while maintaining backend security
      const response = await fetch(`http://localhost:8000/search_similar/?stats=${encodeURIComponent(statsInput)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      setResults(data.results || []);
    } catch (error) {
      console.error('Error searching by stats:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleNameSearch = async (searchName = null) => {
    const searchTerm = searchName || nameInput;
    if (!searchTerm.trim()) return;

    setLoading(true);
    try {
      // Direct API call for name search
      // This bypasses frontend validation while maintaining backend security
      const response = await fetch(`http://localhost:8000/search_by_name/?name=${encodeURIComponent(searchTerm)}&limit=10`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      setResults(data.results || []);
    } catch (error) {
      console.error('Error searching by name:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (searchType === 'name') {
      handleNameSearch();
    } else {
      handleStatsSearch();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  // Helper function to calculate level-adjusted stats
  const calculateLevelStats = (baseStats, level) => {
    const stats = [];
    const statKeys = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'];

    statKeys.forEach((key, index) => {
      const baseStat = baseStats[key];
      if (key === 'hp') {
        // HP formula: ((2 * base + 31) * level / 100) + level + 10
        stats.push(Math.floor(((2 * baseStat + 31) * level / 100) + level + 10));
      } else {
        // Other stats: ((2 * base + 31) * level / 100) + 5
        stats.push(Math.floor(((2 * baseStat + 31) * level / 100) + 5));
      }
    });

    return stats;
  };

  const copyStatsToClipboard = async (pokemon) => {
    // Use level-adjusted stats if in radar mode, otherwise use base stats
    const statsToUse = viewMode === 'radar' ?
      calculateLevelStats(pokemon.metadata.stats, selectedLevel) :
      [
        pokemon.metadata.stats.hp,
        pokemon.metadata.stats.attack,
        pokemon.metadata.stats.defense,
        pokemon.metadata.stats.special_attack,
        pokemon.metadata.stats.special_defense,
        pokemon.metadata.stats.speed
      ];

    const stats = statsToUse.join(',');

    try {
      await navigator.clipboard.writeText(stats);
      // Show a temporary success message
      const button = event.target;
      const originalText = button.textContent;
      button.textContent = '✓ Copied!';
      button.style.background = '#28a745';

      setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '';
      }, 2000);
    } catch (err) {
      console.error('Failed to copy stats:', err);
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = stats;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);

      // Show success message
      const button = event.target;
      const originalText = button.textContent;
      button.textContent = '✓ Copied!';
      button.style.background = '#28a745';

      setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '';
      }, 2000);
    }
  };

  return (
    <div>
      <div className="page-title-container">
        <h2 className="page-title">🔍 Search Pokémon</h2>
      </div>

      <div style={{ marginBottom: '30px' }}>
        <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', marginBottom: '20px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
            <input
              type="radio"
              value="name"
              checked={searchType === 'name'}
              onChange={(e) => setSearchType(e.target.value)}
            />
            <span>Search by Name</span>
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
            <input
              type="radio"
              value="stats"
              checked={searchType === 'stats'}
              onChange={(e) => setSearchType(e.target.value)}
            />
            <span>Search by Stats</span>
          </label>
        </div>

        <button
          className="btn"
          onClick={handleSearch}
          disabled={loading || (!statsInput.trim() && !nameInput.trim())}
          style={{ width: '100%', marginBottom: '20px' }}
        >
          {loading ? 'Searching...' : `🔍 Search ${searchType === 'name' ? 'by Name' : 'Similar Pokémon'}`}
        </button>

        <div style={{ textAlign: 'center', marginBottom: '15px', color: '#666', fontSize: '0.9rem' }}>
          {searchType === 'name' ?
            '👇 Type a Pokémon name below or select from suggestions' :
            '👇 Enter comma-separated stats below'
          }
        </div>

        {searchType === 'name' ? (
          <div className="form-group">
            <label className="form-label">
              Enter Pokémon Name
            </label>
            <PokemonAutocomplete
              placeholder="e.g., Pikachu, Charizard, Bulbasaur..."
              value={nameInput}
              onChange={setNameInput}
              onSelect={(pokemon) => {
                setNameInput(pokemon.name);
                // Auto-search when Pokemon is selected, passing the name directly
                // This ensures we search for the selected Pokemon, not the partial input
                handleNameSearch(pokemon.name);
              }}
            />
          </div>
        ) : (
          <div className="form-group">
            <label className="form-label">
              Enter Pokémon Stats (HP, Attack, Defense, Special Attack, Special Defense, Speed)
            </label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g., 35,55,40,50,50,90 (Pikachu's stats)"
              value={statsInput}
              onChange={(e) => setStatsInput(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <small style={{ color: '#666', fontSize: '0.9rem' }}>
              💡 Try: 35,55,40,50,50,90 (Pikachu) or 45,49,49,65,65,45 (Bulbasaur)
            </small>
          </div>
        )}
      </div>

      {loading && (
        <div className="loading">
          <div className="spinner"></div>
        </div>
      )}

      {results.length > 0 && (
        <div className="search-results">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ margin: 0, color: '#667eea' }}>
              {searchType === 'name' ? 'Search Results:' : 'Similar Pokémon Found:'} ({results.length})
            </h3>

            <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
              {/* Radar chart controls */}
              {viewMode === 'radar' && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                  {/* Radar mode selector */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <label style={{ fontSize: '14px', color: '#666' }}>Mode:</label>
                    <select
                      value={radarMode}
                      onChange={(e) => setRadarMode(e.target.value)}
                      style={{ padding: '4px 8px', borderRadius: '4px', border: '1px solid #ddd', fontSize: '12px' }}
                    >
                      <option value="comparison">Base vs Level</option>
                      <option value="growth">Base + Growth</option>
                      <option value="level-only">Level Only</option>
                    </select>
                  </div>

                  {/* Level selector */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <label style={{ fontSize: '14px', color: '#666' }}>Level:</label>
                    <select
                      value={selectedLevel}
                      onChange={(e) => setSelectedLevel(parseInt(e.target.value))}
                      style={{ padding: '4px 8px', borderRadius: '4px', border: '1px solid #ddd' }}
                    >
                      {[...Array(20)].map((_, i) => {
                        const level = (i + 1) * 5;
                        return <option key={level} value={level}>{level}</option>;
                      })}
                    </select>
                  </div>
                </div>
              )}

              {/* View mode toggle */}
              <div className="pokemon-stats-toggle">
                <button
                  className={`stats-toggle-btn ${viewMode === 'list' ? 'active' : ''}`}
                  onClick={() => setViewMode('list')}
                >
                  📊 List View
                </button>
                <button
                  className={`stats-toggle-btn ${viewMode === 'radar' ? 'active' : ''}`}
                  onClick={() => setViewMode('radar')}
                >
                  🎯 Radar View
                </button>
              </div>
            </div>
          </div>

          <div className="pokemon-grid">
            {results.map((pokemon, idx) => (
              <div key={idx} className="pokemon-card">
                <div className="pokemon-header">
                  <img
                    src={pokemon.metadata.sprite_url}
                    alt={pokemon.name}
                    className="pokemon-sprite"
                  />
                  <h3 className="pokemon-name">{pokemon.name}</h3>
                </div>

                {searchType === 'stats' && pokemon.score && (
                  <div className="similarity-score">
                    Similarity: {(pokemon.score * 100).toFixed(1)}%
                  </div>
                )}

                <div className="pokemon-types">
                  {pokemon.metadata.types.map((type) => (
                    <span key={type} className={`type-badge type-${type}`}>
                      {type}
                    </span>
                  ))}
                </div>

                {/* Conditional rendering based on view mode */}
                {viewMode === 'list' ? (
                  <div className="pokemon-stats">
                    <div className="stat-item">
                      <span className="stat-name">HP:</span>
                      <span className="stat-value">{pokemon.metadata.stats.hp}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-name">Attack:</span>
                      <span className="stat-value">{pokemon.metadata.stats.attack}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-name">Defense:</span>
                      <span className="stat-value">{pokemon.metadata.stats.defense}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-name">Sp. Atk:</span>
                      <span className="stat-value">{pokemon.metadata.stats.special_attack}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-name">Sp. Def:</span>
                      <span className="stat-value">{pokemon.metadata.stats.special_defense}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-name">Speed:</span>
                      <span className="stat-value">{pokemon.metadata.stats.speed}</span>
                    </div>
                  </div>
                ) : (
                  <PokemonRadarChart
                    stats={pokemon.metadata.stats}
                    level={selectedLevel}
                    size={180}
                    mode={radarMode}
                  />
                )}

                {/* Level-adjusted stats display for radar mode */}
                {viewMode === 'radar' && (
                  <div className="level-stats-display">
                    <h4 style={{ margin: '10px 0 5px 0', color: '#667eea', fontSize: '14px' }}>
                      Level {selectedLevel} Stats:
                    </h4>
                    <div className="pokemon-stats" style={{ fontSize: '12px' }}>
                      {(() => {
                        const levelStats = calculateLevelStats(pokemon.metadata.stats, selectedLevel);
                        const statNames = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'];
                        return statNames.map((name, index) => (
                          <div key={name} className="stat-item">
                            <span className="stat-name">{name}:</span>
                            <span className="stat-value">{levelStats[index]}</span>
                          </div>
                        ));
                      })()}
                    </div>
                  </div>
                )}

                <div style={{ marginTop: '15px', fontSize: '0.9rem', color: '#666' }}>
                  <div><strong>Height:</strong> {pokemon.metadata.height / 10}m</div>
                  <div><strong>Weight:</strong> {pokemon.metadata.weight / 10}kg</div>
                  <div><strong>Base Exp:</strong> {pokemon.metadata.base_experience}</div>
                </div>

                <div className="stats-format">
                  <strong>Stats{viewMode === 'radar' ? ` (Level ${selectedLevel})` : ' (Base)'}:</strong> {
                    viewMode === 'radar' ?
                      calculateLevelStats(pokemon.metadata.stats, selectedLevel).join(',') :
                      [
                        pokemon.metadata.stats.hp,
                        pokemon.metadata.stats.attack,
                        pokemon.metadata.stats.defense,
                        pokemon.metadata.stats.special_attack,
                        pokemon.metadata.stats.special_defense,
                        pokemon.metadata.stats.speed
                      ].join(',')
                  }
                </div>

                <button
                  className="copy-btn"
                  onClick={() => copyStatsToClipboard(pokemon)}
                >
                  📋 Copy Stats for Search
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {!loading && results.length === 0 && (statsInput.trim() || nameInput.trim()) && (
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          <div style={{ fontSize: '3rem', marginBottom: '15px' }}>😔</div>
          <p>No Pokémon found. Try a different search term!</p>
        </div>
      )}
    </div>
  );
}

export default Search;
