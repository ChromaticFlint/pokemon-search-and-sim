import React, { useState, useEffect } from 'react';

function Skills() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedMove, setSelectedMove] = useState(null);
  const [moveDetails, setMoveDetails] = useState(null);

  // Sample move categories for quick search
  const moveCategories = [
    { name: 'High Power', query: 'powerful devastating strong high damage' },
    { name: 'Status Effects', query: 'paralysis burn freeze sleep poison' },
    { name: 'Critical Hits', query: 'critical hit high crit ratio' },
    { name: 'Accuracy Issues', query: 'low accuracy miss unreliable' },
    { name: 'Type Coverage', query: 'super effective coverage weakness' },
    { name: 'Physical Attacks', query: 'physical attack melee contact' },
    { name: 'Special Attacks', query: 'special attack ranged projectile' },
    { name: 'Defensive Moves', query: 'protect defend shield barrier' }
  ];

  const searchMoves = async (query) => {
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    setLoading(true);
    try {
      // Search for moves using the vector database
      const response = await fetch(`http://localhost:8000/search_moves/?query=${encodeURIComponent(query)}&limit=20`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setSearchResults(data.results || []);
    } catch (error) {
      console.error('Error searching moves:', error);
      setSearchResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    searchMoves(searchQuery);
  };

  const handleCategorySearch = (query) => {
    setSearchQuery(query);
    searchMoves(query);
  };

  const getMoveDetails = async (moveName) => {
    try {
      const response = await fetch(`http://localhost:8000/move_details/?name=${encodeURIComponent(moveName)}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setMoveDetails(data);
    } catch (error) {
      console.error('Error getting move details:', error);
      setMoveDetails(null);
    }
  };

  const handleMoveSelect = (move) => {
    setSelectedMove(move);
    getMoveDetails(move.name);
  };

  return (
    <div>
      <h1>🎯 Pokemon Skills & Moves</h1>

      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <p style={{ fontSize: '1.2rem', color: '#666', lineHeight: '1.6' }}>
          Discover powerful moves and learn about Pokemon abilities using AI-powered search
        </p>
      </div>

      {/* Search Section */}
      <div className="search-section">
        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-group">
            <input
              type="text"
              className="search-input"
              placeholder="Search for moves... (e.g., 'powerful electric attacks', 'status moves', 'high critical hit')"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="search-button" disabled={loading}>
              {loading ? '🔄' : '🔍'} Search
            </button>
          </div>
        </form>

        {/* Quick Category Buttons */}
        <div className="category-buttons">
          <h3>Quick Search Categories:</h3>
          <div className="button-grid">
            {moveCategories.map((category) => (
              <button
                key={category.name}
                className="category-button"
                onClick={() => handleCategorySearch(category.query)}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results Section */}
      <div className="results-section">
        {loading && (
          <div className="loading">
            <div className="loading-spinner"></div>
            <p>Searching Pokemon moves...</p>
          </div>
        )}

        {searchResults.length > 0 && (
          <div className="search-results">
            <h2>Search Results ({searchResults.length} moves found)</h2>
            <div className="moves-grid">
              {searchResults.map((move, index) => (
                <div
                  key={index}
                  className={`move-card ${selectedMove?.name === move.name ? 'selected' : ''}`}
                  onClick={() => handleMoveSelect(move)}
                >
                  <div className="move-header">
                    <h3>{move.name}</h3>
                    <span className={`type-badge type-${move.type}`}>{move.type}</span>
                  </div>
                  <div className="move-stats">
                    <div className="stat">
                      <span className="stat-label">Power:</span>
                      <span className="stat-value">{move.power || 'N/A'}</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Accuracy:</span>
                      <span className="stat-value">{move.accuracy}%</span>
                    </div>
                    <div className="stat">
                      <span className="stat-label">Category:</span>
                      <span className="stat-value">{move.category}</span>
                    </div>
                  </div>
                  <div className="move-description">
                    {move.description || 'Click for more details...'}
                  </div>
                  <div className="similarity-score">
                    Relevance: {(move.similarity * 100).toFixed(1)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Move Details Panel */}
        {selectedMove && moveDetails && (
          <div className="move-details-panel">
            <h2>📋 Move Details: {selectedMove.name}</h2>
            <div className="move-details-content">
              <div className="move-info">
                <div className="detail-row">
                  <span className="detail-label">Type:</span>
                  <span className={`type-badge type-${moveDetails.type}`}>{moveDetails.type}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Category:</span>
                  <span className="detail-value">{moveDetails.category}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Power:</span>
                  <span className="detail-value">{moveDetails.power || 'N/A'}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Accuracy:</span>
                  <span className="detail-value">{moveDetails.accuracy}%</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">PP:</span>
                  <span className="detail-value">{moveDetails.pp}</span>
                </div>
                {moveDetails.effect && (
                  <div className="detail-row">
                    <span className="detail-label">Effect:</span>
                    <span className="detail-value">{moveDetails.effect}</span>
                  </div>
                )}
              </div>
              
              <div className="pokemon-learners">
                <h3>Pokemon that can learn this move:</h3>
                <div className="pokemon-list">
                  {moveDetails.learners?.map((pokemon, index) => (
                    <div key={index} className="pokemon-learner">
                      <img 
                        src={pokemon.sprite_url} 
                        alt={pokemon.name}
                        className="pokemon-sprite-small"
                      />
                      <span>{pokemon.name}</span>
                    </div>
                  )) || <p>Loading Pokemon data...</p>}
                </div>
              </div>
            </div>
          </div>
        )}

        {searchQuery && !loading && searchResults.length === 0 && (
          <div className="no-results">
            <h3>No moves found</h3>
            <p>Try searching for different terms like "fire attacks", "status moves", or "high power"</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Skills;
