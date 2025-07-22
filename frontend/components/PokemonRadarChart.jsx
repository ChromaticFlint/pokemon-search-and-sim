import React from 'react';

const PokemonRadarChart = ({ stats, level = 50, size = 200, mode = 'comparison' }) => {
  // mode options: 'comparison' (base vs level), 'growth' (base + growth overlay), 'level-only' (just level stats)
  // Pokemon stat names and their order for the radar chart
  const statNames = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'];
  const statKeys = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'];
  
  // Maximum possible stat values for normalization (approximate Pokemon maximums)
  const maxStats = {
    hp: 255,        // Blissey's HP
    attack: 190,    // Mega Mewtwo X's Attack
    defense: 230,   // Shuckle's Defense
    special_attack: 194,  // Mega Mewtwo Y's Special Attack
    special_defense: 230, // Shuckle's Special Defense
    speed: 180      // Ninjask's Speed
  };

  // Calculate level-adjusted stats using Pokemon formula
  const calculateLevelStats = (baseStats, level) => {
    return statKeys.map(key => {
      const baseStat = baseStats[key];
      if (key === 'hp') {
        // HP formula: ((2 * base + IV + EV/4) * level / 100) + level + 10
        return Math.floor(((2 * baseStat + 31) * level / 100) + level + 10);
      } else {
        // Other stats: ((2 * base + IV + EV/4) * level / 100) + 5
        return Math.floor(((2 * baseStat + 31) * level / 100) + 5);
      }
    });
  };

  // Get base stats and level-adjusted stats
  const baseStats = statKeys.map(key => stats[key]);
  const levelStats = calculateLevelStats(stats, level);

  // Calculate growth amounts (difference between level stats and base stats)
  const growthStats = levelStats.map((levelStat, index) => levelStat - baseStats[index]);

  // Chart configuration
  const center = size / 2;
  const radius = (size / 2) - 30;
  const angleStep = (2 * Math.PI) / 6; // 6 stats

  // Generate points for the hexagon grid
  const generateGridPoints = (radiusMultiplier) => {
    return statKeys.map((_, index) => {
      const angle = index * angleStep - Math.PI / 2; // Start from top
      const x = center + Math.cos(angle) * radius * radiusMultiplier;
      const y = center + Math.sin(angle) * radius * radiusMultiplier;
      return { x, y };
    });
  };

  // Generate stat points for base and level stats
  const generateStatPoints = (statValues, isLevel = false) => {
    return statValues.map((value, index) => {
      const maxValue = isLevel ? maxStats[statKeys[index]] * 2 : maxStats[statKeys[index]]; // Level stats can be higher
      const normalizedValue = Math.min(value / maxValue, 1); // Normalize to 0-1
      const angle = index * angleStep - Math.PI / 2;
      const x = center + Math.cos(angle) * radius * normalizedValue;
      const y = center + Math.sin(angle) * radius * normalizedValue;
      return { x, y };
    });
  };

  // Generate label positions
  const generateLabelPoints = () => {
    return statNames.map((name, index) => {
      const angle = index * angleStep - Math.PI / 2;
      const labelRadius = radius + 20;
      const x = center + Math.cos(angle) * labelRadius;
      const y = center + Math.sin(angle) * labelRadius;
      return { x, y, name };
    });
  };

  // Create path strings for the stat polygons
  const createPath = (points) => {
    return points.map((point, index) =>
      `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`
    ).join(' ') + ' Z';
  };

  // Generate points based on mode
  let primaryPoints, secondaryPoints, primaryPath, secondaryPath;
  let primaryColor, secondaryColor, primaryLabel, secondaryLabel;

  if (mode === 'comparison') {
    // Base stats vs Level stats
    primaryPoints = generateStatPoints(baseStats, false);
    secondaryPoints = generateStatPoints(levelStats, true);
    primaryColor = { fill: 'rgba(76, 175, 80, 0.3)', stroke: 'rgba(76, 175, 80, 0.8)' };
    secondaryColor = { fill: 'rgba(33, 150, 243, 0.2)', stroke: 'rgba(33, 150, 243, 0.8)' };
    primaryLabel = 'Base Stats';
    secondaryLabel = `Lv.${level} Stats`;
  } else if (mode === 'growth') {
    // Base stats + Growth overlay (additive visualization)
    primaryPoints = generateStatPoints(baseStats, false);
    secondaryPoints = generateStatPoints(growthStats.map((growth, i) => baseStats[i] + growth), true);
    primaryColor = { fill: 'rgba(76, 175, 80, 0.4)', stroke: 'rgba(76, 175, 80, 0.9)' };
    secondaryColor = { fill: 'rgba(255, 193, 7, 0.3)', stroke: 'rgba(255, 193, 7, 0.8)' };
    primaryLabel = 'Base Stats';
    secondaryLabel = `+Growth (Lv.${level})`;
  } else {
    // Level-only mode
    primaryPoints = generateStatPoints(baseStats, false);
    secondaryPoints = generateStatPoints(levelStats, true);
    primaryColor = { fill: 'rgba(200, 200, 200, 0.2)', stroke: 'rgba(200, 200, 200, 0.5)' };
    secondaryColor = { fill: 'rgba(33, 150, 243, 0.3)', stroke: 'rgba(33, 150, 243, 0.8)' };
    primaryLabel = 'Base Reference';
    secondaryLabel = `Lv.${level} Stats`;
  }

  primaryPath = createPath(primaryPoints);
  secondaryPath = createPath(secondaryPoints);
  const labelPoints = generateLabelPoints();

  return (
    <div className="pokemon-radar-chart">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        style={{ maxWidth: '100%', height: 'auto' }}
      >
        {/* Background grid circles */}
        {[0.2, 0.4, 0.6, 0.8, 1.0].map((multiplier, index) => (
          <circle
            key={index}
            cx={center}
            cy={center}
            r={radius * multiplier}
            fill="none"
            stroke="#e0e0e0"
            strokeWidth="1"
            opacity="0.5"
          />
        ))}

        {/* Grid lines from center to each stat */}
        {generateGridPoints(1).map((point, index) => (
          <line
            key={index}
            x1={center}
            y1={center}
            x2={point.x}
            y2={point.y}
            stroke="#e0e0e0"
            strokeWidth="1"
            opacity="0.5"
          />
        ))}

        {/* Primary stats area */}
        <path
          d={primaryPath}
          fill={primaryColor.fill}
          stroke={primaryColor.stroke}
          strokeWidth="2"
          style={{
            animation: 'fadeIn 0.8s ease-in-out',
            transformOrigin: 'center'
          }}
        />

        {/* Secondary stats area */}
        <path
          d={secondaryPath}
          fill={secondaryColor.fill}
          stroke={secondaryColor.stroke}
          strokeWidth="2"
          style={{
            animation: 'fadeIn 1.2s ease-in-out',
            transformOrigin: 'center'
          }}
        />

        {/* Primary stat points */}
        {primaryPoints.map((point, index) => (
          <circle
            key={`primary-${index}`}
            cx={point.x}
            cy={point.y}
            r="3"
            fill={primaryColor.stroke}
          />
        ))}

        {/* Secondary stat points */}
        {secondaryPoints.map((point, index) => (
          <circle
            key={`secondary-${index}`}
            cx={point.x}
            cy={point.y}
            r="3"
            fill={secondaryColor.stroke}
          />
        ))}

        {/* Stat labels */}
        {labelPoints.map((label, index) => (
          <text
            key={index}
            x={label.x}
            y={label.y}
            textAnchor="middle"
            dominantBaseline="middle"
            fontSize="11"
            fill="#333"
            fontWeight="600"
          >
            {label.name}
          </text>
        ))}
      </svg>

      {/* Legend */}
      <div className="radar-legend">
        <div className="legend-item">
          <div
            className="legend-color"
            style={{
              background: primaryColor.fill,
              border: `1px solid ${primaryColor.stroke}`
            }}
          ></div>
          <span>{primaryLabel}</span>
        </div>
        <div className="legend-item">
          <div
            className="legend-color"
            style={{
              background: secondaryColor.fill,
              border: `1px solid ${secondaryColor.stroke}`
            }}
          ></div>
          <span>{secondaryLabel}</span>
        </div>
      </div>

      {/* Stat values display */}
      <div className="radar-stats">
        {statNames.map((name, index) => {
          let leftValue, rightValue, showArrow = true;

          if (mode === 'comparison') {
            leftValue = baseStats[index];
            rightValue = levelStats[index];
          } else if (mode === 'growth') {
            leftValue = baseStats[index];
            rightValue = `+${growthStats[index]}`;
          } else {
            leftValue = baseStats[index];
            rightValue = levelStats[index];
          }

          return (
            <div key={index} className="radar-stat-item">
              <span className="radar-stat-name">{name}:</span>
              <span className="radar-stat-base">{leftValue}</span>
              {showArrow && <span className="radar-stat-arrow">→</span>}
              <span className="radar-stat-level">{rightValue}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default PokemonRadarChart;
