import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import PokemonRadarChart from './PokemonRadarChart';

function Home() {
  const [featuredPokemon, setFeaturedPokemon] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('list'); // 'list' or 'radar'
  const [selectedLevel, setSelectedLevel] = useState(50);
  const [radarMode, setRadarMode] = useState('comparison'); // 'comparison', 'growth', 'level-only'
  const navigate = useNavigate();

  useEffect(() => {
    const loadFeaturedPokemon = async () => {
      try {
        // Direct API call for featured Pokemon
        // This bypasses frontend validation while maintaining backend security
        const response = await fetch('http://localhost:8000/pokemon/top/?criteria=power&limit=6');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        setFeaturedPokemon(data.results || []);
      } catch (error) {
        console.error('Error loading featured Pokemon:', error);
      } finally {
        setLoading(false);
      }
    };

    loadFeaturedPokemon();
  }, []);

  const copyStatsToClipboard = async (pokemon) => {
    const stats = [
      pokemon.metadata.stats.hp,
      pokemon.metadata.stats.attack,
      pokemon.metadata.stats.defense,
      pokemon.metadata.stats.special_attack,
      pokemon.metadata.stats.special_defense,
      pokemon.metadata.stats.speed
    ].join(',');

    try {
      await navigator.clipboard.writeText(stats);
      // Show a temporary success message
      const button = event.target;
      const originalText = button.textContent;
      button.textContent = '✓ Copied!';
      button.classList.add('success');

      setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('success');
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
      button.classList.add('success');

      setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('success');
      }, 2000);
    }
  };

  return (
    <div>
      <h1>🌟 Pokémon Search & Battle Arena</h1>

      <div style={{ textAlign: 'center', marginBottom: '40px' }}>
        <p style={{ fontSize: '1.2rem', color: '#666', lineHeight: '1.6' }}>
          Discover Pokémon with similar stats using advanced vector similarity search,
          and simulate epic battles based on authentic base stats from the Pokémon universe!
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '30px', marginBottom: '40px' }}>
        <div
          className="feature-card"
          onClick={() => navigate('/search')}
          onKeyDown={(e) => e.key === 'Enter' && navigate('/search')}
          tabIndex={0}
          role="button"
          aria-label="Navigate to Smart Search page"
        >
          <div className="feature-icon">🔍</div>
          <h3 className="feature-title">Smart Search</h3>
          <p className="feature-description">Find Pokémon with similar stat distributions using our vector database technology</p>
          <div className="feature-cta">Click to explore →</div>
        </div>

        <div
          className="feature-card"
          onClick={() => navigate('/battle')}
          onKeyDown={(e) => e.key === 'Enter' && navigate('/battle')}
          tabIndex={0}
          role="button"
          aria-label="Navigate to Battle Simulator page"
        >
          <div className="feature-icon">⚔️</div>
          <h3 className="feature-title">Battle Simulator</h3>
          <p className="feature-description">Simulate battles between any Pokémon with type effectiveness and realistic combat</p>
          <div className="feature-cta">Click to battle →</div>
        </div>

        <div
          className="feature-card"
          onClick={() => navigate('/rankings')}
          onKeyDown={(e) => e.key === 'Enter' && navigate('/rankings')}
          tabIndex={0}
          role="button"
          aria-label="Navigate to Rankings page"
        >
          <div className="feature-icon">📊</div>
          <h3 className="feature-title">Rich Data & Rankings</h3>
          <p className="feature-description">Explore Pokémon rankings across different categories with complete data and statistics</p>
          <div className="feature-cta">Click to view rankings →</div>
        </div>
      </div>

      <h2 style={{ textAlign: 'center', marginBottom: '30px' }}>🏆 Top Pokémon by Power Rating</h2>

      {loading ? (
        <div className="loading">
          <div className="spinner"></div>
        </div>
      ) : (
        <div className="pokemon-grid">
          {featuredPokemon.map((pokemon, index) => (
            <div key={pokemon.id} className="pokemon-card">
              <div style={{ position: 'relative' }}>
                <div style={{
                  position: 'absolute',
                  top: '-10px',
                  right: '-10px',
                  background: 'linear-gradient(135deg, #ffd700, #ffed4e)',
                  color: '#333',
                  borderRadius: '50%',
                  width: '30px',
                  height: '30px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 'bold',
                  fontSize: '0.9rem',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.2)'
                }}>
                  #{index + 1}
                </div>

                <div className="pokemon-header">
                  <img
                    src={pokemon.metadata.sprite_url}
                    alt={pokemon.name}
                    className="pokemon-sprite"
                  />
                  <div>
                    <h3 className="pokemon-name">{pokemon.name}</h3>
                    <div style={{ fontSize: '0.9rem', color: '#667eea', fontWeight: '600' }}>
                      Power: {pokemon.power_score} | Total: {pokemon.total_stats}
                    </div>
                  </div>
                </div>
              </div>

              <div className="pokemon-types">
                {pokemon.metadata.types.map((type) => (
                  <span key={type} className={`type-badge type-${type}`}>
                    {type}
                  </span>
                ))}
              </div>

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

              <div className="stats-format">
                <strong>Stats:</strong> {[
                  pokemon.metadata.stats.hp,
                  pokemon.metadata.stats.attack,
                  pokemon.metadata.stats.defense,
                  pokemon.metadata.stats.special_attack,
                  pokemon.metadata.stats.special_defense,
                  pokemon.metadata.stats.speed
                ].join(',')}
              </div>

              <button
                className="copy-btn"
                onClick={() => copyStatsToClipboard(pokemon)}
              >
                📋 Copy Stats
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Home;
