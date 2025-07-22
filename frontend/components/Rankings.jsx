import { useState, useEffect } from 'react';

function Rankings() {
  const [rankings, setRankings] = useState({});
  const [activeTab, setActiveTab] = useState('power');
  const [loading, setLoading] = useState(true);

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
          // Direct API call for rankings
          // This bypasses frontend validation while maintaining backend security
          const response = await fetch(`http://localhost:8000/pokemon/top/?criteria=${criteria}&limit=10`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const data = await response.json();

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
      <h2>📈 Pokémon Rankings</h2>
      
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
        marginBottom: '30px',
        padding: '15px',
        background: 'rgba(102, 126, 234, 0.1)',
        borderRadius: '10px',
        color: '#667eea',
        fontWeight: '600'
      }}>
        {rankingTypes[activeTab].description}
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
