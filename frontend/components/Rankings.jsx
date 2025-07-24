import { useState, useEffect } from 'react';
import { getTopPokemon } from '../api.js';
import PokemonRadarChart from './PokemonRadarChart';

function Rankings() {
  const [rankings, setRankings] = useState({});
  const [activeTab, setActiveTab] = useState('power');
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('list'); // 'list' or 'radar'
  const [selectedLevel, setSelectedLevel] = useState(50);
  const [radarMode, setRadarMode] = useState('comparison'); // 'comparison', 'growth', 'level-only'

  const rankingTypes = {
    power: { label: '🏆 Power Rating', description: 'Weighted score favoring offensive stats' },
    total: { label: '📊 Total Stats', description: 'Sum of all base stats' },
    offensive: { label: '⚔️ Offensive', description: 'Attack + Special Attack + Speed bonus' },
    defensive: { label: '🛡️ Defensive', description: 'HP + Defense + Special Defense' },
    speed: { label: '💨 Speed', description: 'Fastest Pokemon' }
  };

  useEffect(() => {
    const loadAllRankings = async () => {
      setLoading(true);
      try {
        const rankingData = {};

        for (const criteria of Object.keys(rankingTypes)) {
          const data = await getTopPokemon(criteria, 10);
          rankingData[criteria] = data.results || [];
        }

        setRankings(rankingData);
      } catch (error) {
        console.error('Error loading rankings:', error);
      } finally {
        setLoading(false);
      }
    };

    loadAllRankings();
  }, []);

  // Helper function to calculate level-adjusted stats
  const calculateLevelStats = (baseStats, level) => {
    const stats = [];
    const statKeys = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'];

    statKeys.forEach((key) => {
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
    }
  };

  const getRankingIcon = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  return (
    <div>
      <div className="page-title-container">
        <h2 className="page-title">📈 Pokémon Rankings</h2>
      </div>
      
      <p style={{ textAlign: 'center', color: '#666', marginBottom: '40px', fontSize: '1.1rem' }}>
        Discover the strongest Pokémon across different categories based on their base stats!
      </p>

      {/* Ranking Tabs */}
      <div style={{ 
        display: 'flex', 
        gap: '10px', 
        marginBottom: '30px', 
        flexWrap: 'wrap',
        justifyContent: 'center'
      }}>
        {Object.entries(rankingTypes).map(([key, info]) => (
          <button
            key={key}
            onClick={() => setActiveTab(key)}
            style={{
              padding: '12px 20px',
              border: 'none',
              borderRadius: '25px',
              background: activeTab === key 
                ? 'linear-gradient(135deg, #667eea, #764ba2)' 
                : 'rgba(102, 126, 234, 0.1)',
              color: activeTab === key ? 'white' : '#667eea',
              fontWeight: '600',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              fontSize: '0.9rem'
            }}
            onMouseOver={(e) => {
              if (activeTab !== key) {
                e.target.style.background = 'rgba(102, 126, 234, 0.2)';
              }
            }}
            onMouseOut={(e) => {
              if (activeTab !== key) {
                e.target.style.background = 'rgba(102, 126, 234, 0.1)';
              }
            }}
          >
            {info.label}
          </button>
        ))}
      </div>

      {/* Active Ranking Description */}
      <div style={{
        textAlign: 'center',
        marginBottom: '20px',
        padding: '15px',
        background: 'rgba(102, 126, 234, 0.1)',
        borderRadius: '10px',
        color: '#667eea',
        fontWeight: '600'
      }}>
        {rankingTypes[activeTab].description}
      </div>

      {/* View Controls */}
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '15px', marginBottom: '30px' }}>
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

      {loading ? (
        <div className="loading">
          <div className="spinner"></div>
        </div>
      ) : (
        <div className="pokemon-grid">
          {rankings[activeTab]?.map((pokemon, index) => (
            <div key={pokemon.id} className="pokemon-card">
              <div style={{ position: 'relative' }}>
                <div style={{ 
                  position: 'absolute', 
                  top: '-10px', 
                  left: '-10px', 
                  background: index < 3 
                    ? 'linear-gradient(135deg, #ffd700, #ffed4e)' 
                    : 'linear-gradient(135deg, #667eea, #764ba2)', 
                  color: index < 3 ? '#333' : 'white', 
                  borderRadius: '50%', 
                  width: '35px', 
                  height: '35px', 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center', 
                  fontWeight: 'bold',
                  fontSize: '0.9rem',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
                  zIndex: 1
                }}>
                  {getRankingIcon(index + 1)}
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
                      Score: {pokemon.ranking_score.toFixed(1)} | Total: {pokemon.total_stats}
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
              
              <div style={{ marginTop: '15px', fontSize: '0.9rem', color: '#666' }}>
                <div><strong>Height:</strong> {pokemon.metadata.height / 10}m</div>
                <div><strong>Weight:</strong> {pokemon.metadata.weight / 10}kg</div>
                <div><strong>Base Exp:</strong> {pokemon.metadata.base_experience}</div>
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

      <div style={{ marginTop: '40px', padding: '20px', background: 'rgba(102, 126, 234, 0.1)', borderRadius: '15px' }}>
        <h3 style={{ color: '#667eea', marginBottom: '15px' }}>📊 Ranking Methodology:</h3>
        <ul style={{ color: '#666', lineHeight: '1.6' }}>
          <li><strong>Power Rating:</strong> Weighted score that values offensive stats (Attack, Special Attack) and Speed higher</li>
          <li><strong>Total Stats:</strong> Simple sum of all six base stats (HP + Attack + Defense + Special Attack + Special Defense + Speed)</li>
          <li><strong>Offensive:</strong> Focuses on damage-dealing capability (Attack + Special Attack + Speed bonus)</li>
          <li><strong>Defensive:</strong> Emphasizes survivability (HP + Defense + Special Defense)</li>
          <li><strong>Speed:</strong> Pure speed ranking for determining turn order</li>
        </ul>
      </div>
    </div>
  );
}

export default Rankings;
