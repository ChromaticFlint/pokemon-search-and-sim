import React, { useState } from 'react';
import { simulateBattle, searchByName, battleAdvanced } from '../api';
import PokemonAutocomplete from './PokemonAutocomplete';

function Battle() {
  const [pokemonA, setPokemonA] = useState({ name: '', stats: '', data: null });
  const [pokemonB, setPokemonB] = useState({ name: '', stats: '', data: null });
  const [result, setResult] = useState('');
  const [battleLog, setBattleLog] = useState([]);
  const [battleMode, setBattleMode] = useState('simple'); // 'simple' or 'advanced'
  const [loading, setLoading] = useState(false);
  const [searchingA, setSearchingA] = useState(false);
  const [searchingB, setSearchingB] = useState(false);



  const handleBattle = async () => {
    if (battleMode === 'advanced') {
      // Advanced battle requires Pokemon names
      if (!pokemonA.data || !pokemonB.data) {
        alert('Please search for both Pokémon by name for advanced battle!');
        return;
      }

      setLoading(true);
      try {
        const data = await battleAdvanced(pokemonA.data.name, pokemonB.data.name);
        if (data.error) {
          alert(data.error);
          return;
        }
        setResult(data.battle_result.result);
        setBattleLog(data.battle_result.battle_log || []);
      } catch (error) {
        console.error('Error simulating advanced battle:', error);
        alert('Error simulating advanced battle');
      } finally {
        setLoading(false);
      }
    } else {
      // Simple battle
      if (!pokemonA.stats || !pokemonB.stats) {
        alert('Please enter stats for both Pokémon!');
        return;
      }

      setLoading(true);
      try {
        const data = await simulateBattle(pokemonA.stats, pokemonB.stats);
        setResult(data.result);
        setBattleLog([]);
      } catch (error) {
        console.error('Error simulating battle:', error);
        alert('Error simulating battle');
      } finally {
        setLoading(false);
      }
    }
  };

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

  const PokemonBattleCard = ({ pokemon, setPokemon, searching, setSearching, label }) => (
    <div className="battle-pokemon">
      <h3 style={{ color: '#667eea', marginBottom: '20px' }}>{label}</h3>

      <div className="form-group">
        <label className="form-label">Search by Name</label>
        <PokemonAutocomplete
          placeholder="e.g., Pikachu"
          value={pokemon.name}
          onChange={(name) => setPokemon({ ...pokemon, name })}
          onSelect={(selectedPokemon) => {
            const stats = [
              selectedPokemon.metadata.stats.hp,
              selectedPokemon.metadata.stats.attack,
              selectedPokemon.metadata.stats.defense,
              selectedPokemon.metadata.stats.special_attack,
              selectedPokemon.metadata.stats.special_defense,
              selectedPokemon.metadata.stats.speed
            ].join(',');

            setPokemon({
              name: selectedPokemon.name,
              stats: stats,
              data: selectedPokemon
            });
          }}
          disabled={searching}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Or Enter Stats Manually</label>
        <input
          type="text"
          className="form-input"
          placeholder="HP,Atk,Def,SpA,SpD,Speed"
          value={pokemon.stats}
          onChange={(e) => setPokemon({ ...pokemon, stats: e.target.value, data: null })}
        />
      </div>

      {pokemon.data && (
        <div className="pokemon-card" style={{ marginTop: '20px' }}>
          <div className="pokemon-header">
            <img
              src={pokemon.data.metadata.sprite_url}
              alt={pokemon.data.name}
              className="pokemon-sprite"
            />
            <h3 className="pokemon-name">{pokemon.data.name}</h3>
          </div>

          <div className="pokemon-types">
            {pokemon.data.metadata.types.map((type) => (
              <span key={type} className={`type-badge type-${type}`}>
                {type}
              </span>
            ))}
          </div>

          <div className="pokemon-stats">
            <div className="stat-item">
              <span className="stat-name">HP:</span>
              <span className="stat-value">{pokemon.data.metadata.stats.hp}</span>
            </div>
            <div className="stat-item">
              <span className="stat-name">Attack:</span>
              <span className="stat-value">{pokemon.data.metadata.stats.attack}</span>
            </div>
            <div className="stat-item">
              <span className="stat-name">Defense:</span>
              <span className="stat-value">{pokemon.data.metadata.stats.defense}</span>
            </div>
            <div className="stat-item">
              <span className="stat-name">Sp. Atk:</span>
              <span className="stat-value">{pokemon.data.metadata.stats.special_attack}</span>
            </div>
            <div className="stat-item">
              <span className="stat-name">Sp. Def:</span>
              <span className="stat-value">{pokemon.data.metadata.stats.special_defense}</span>
            </div>
            <div className="stat-item">
              <span className="stat-name">Speed:</span>
              <span className="stat-value">{pokemon.data.metadata.stats.speed}</span>
            </div>
          </div>

          <div className="stats-format">
            <strong>Stats:</strong> {[
              pokemon.data.metadata.stats.hp,
              pokemon.data.metadata.stats.attack,
              pokemon.data.metadata.stats.defense,
              pokemon.data.metadata.stats.special_attack,
              pokemon.data.metadata.stats.special_defense,
              pokemon.data.metadata.stats.speed
            ].join(',')}
          </div>

          <button
            className="copy-btn"
            onClick={() => copyStatsToClipboard(pokemon.data)}
          >
            📋 Copy Stats
          </button>
        </div>
      )}
    </div>
  );

  return (
    <div>
      <h2>⚔️ Battle Simulator</h2>

      <p style={{ textAlign: 'center', color: '#666', marginBottom: '20px', fontSize: '1.1rem' }}>
        Choose two Pokémon and simulate an epic battle!
      </p>

      {/* Battle Mode Selector */}
      <div style={{
        display: 'flex',
        gap: '20px',
        justifyContent: 'center',
        marginBottom: '40px',
        flexWrap: 'wrap'
      }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
          <input
            type="radio"
            value="simple"
            checked={battleMode === 'simple'}
            onChange={(e) => setBattleMode(e.target.value)}
          />
          <span style={{ fontWeight: '600', color: '#667eea' }}>⚡ Simple Battle (Stats Only)</span>
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
          <input
            type="radio"
            value="advanced"
            checked={battleMode === 'advanced'}
            onChange={(e) => setBattleMode(e.target.value)}
          />
          <span style={{ fontWeight: '600', color: '#667eea' }}>🔥 Advanced Battle (Type Effectiveness)</span>
        </label>
      </div>

      <div style={{
        textAlign: 'center',
        marginBottom: '30px',
        padding: '15px',
        background: 'rgba(102, 126, 234, 0.1)',
        borderRadius: '10px',
        color: '#667eea',
        fontWeight: '600'
      }}>
        {battleMode === 'simple'
          ? "📊 Simple battle compares total base stats"
          : "🎯 Advanced battle includes type effectiveness, turn order, and realistic damage calculation"
        }
      </div>

      <div className="battle-container">
        <PokemonBattleCard
          pokemon={pokemonA}
          setPokemon={setPokemonA}
          searching={searchingA}
          setSearching={setSearchingA}
          label="Pokémon A"
        />

        <div className="vs-divider">VS</div>

        <PokemonBattleCard
          pokemon={pokemonB}
          setPokemon={setPokemonB}
          searching={searchingB}
          setSearching={setSearchingB}
          label="Pokémon B"
        />
      </div>

      <div style={{ textAlign: 'center', margin: '40px 0' }}>
        <button
          className="btn"
          onClick={handleBattle}
          disabled={loading ||
            (battleMode === 'simple' && (!pokemonA.stats || !pokemonB.stats)) ||
            (battleMode === 'advanced' && (!pokemonA.data || !pokemonB.data))
          }
          style={{ fontSize: '1.2rem', padding: '20px 40px' }}
        >
          {loading ? 'Battling...' :
           battleMode === 'advanced' ? '🔥 Start Advanced Battle!' : '⚔️ Start Simple Battle!'}
        </button>
      </div>

      {result && (
        <div className="battle-result">
          <div style={{ fontSize: '1.5rem', marginBottom: '10px' }}>🏆 Battle Result</div>
          <div>{result}</div>
          {pokemonA.data && pokemonB.data && (
            <div style={{ marginTop: '15px', fontSize: '1rem' }}>
              {pokemonA.data.name} vs {pokemonB.data.name}
            </div>
          )}
        </div>
      )}

      {/* Battle Log for Advanced Battles */}
      {battleLog.length > 0 && (
        <div style={{
          marginTop: '30px',
          padding: '20px',
          background: 'rgba(255, 255, 255, 0.95)',
          borderRadius: '15px',
          boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)'
        }}>
          <h3 style={{ color: '#667eea', marginBottom: '20px', textAlign: 'center' }}>
            📜 Battle Log
          </h3>
          <div style={{
            maxHeight: '400px',
            overflowY: 'auto',
            fontFamily: 'monospace',
            fontSize: '0.9rem',
            lineHeight: '1.6',
            background: '#f8f9fa',
            padding: '15px',
            borderRadius: '8px',
            border: '1px solid #e1e5e9'
          }}>
            {battleLog.map((logEntry, index) => (
              <div key={index} style={{
                marginBottom: '5px',
                color: logEntry.includes('🏆') ? '#28a745' :
                      logEntry.includes('⚔️') ? '#dc3545' :
                      logEntry.includes('💚') ? '#28a745' :
                      logEntry.includes('📊') ? '#6f42c1' : '#333'
              }}>
                {logEntry}
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ marginTop: '40px', padding: '20px', background: 'rgba(102, 126, 234, 0.1)', borderRadius: '15px' }}>
        <h3 style={{ color: '#667eea', marginBottom: '15px' }}>💡 How it works:</h3>
        <ul style={{ color: '#666', lineHeight: '1.6' }}>
          <li>The battle simulator compares the total base stats of both Pokémon</li>
          <li>The Pokémon with higher total stats wins the battle</li>
          <li>In case of a tie, the battle results in a draw</li>
          <li>You can search by name or enter custom stats manually</li>
        </ul>
      </div>
    </div>
  );
}

export default Battle;
