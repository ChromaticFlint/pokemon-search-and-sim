import { createContext, useContext, useState, useEffect } from 'react';
import { getAllPokemon } from '../api.js';

// Create Pokemon data context
const PokemonContext = createContext();

// Pokemon data provider component
export function PokemonProvider({ children }) {
  const [allPokemon, setAllPokemon] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load all Pokemon data once when provider mounts
  useEffect(() => {
    const loadPokemon = async () => {
      try {
        const data = await getAllPokemon(1000);
        setAllPokemon(data.results || []);
        setError(null);
      } catch (err) {
        console.error('Error loading Pokemon for autocomplete:', err);
        setError(err.message);
        setAllPokemon([]);
      } finally {
        setLoading(false);
      }
    };

    loadPokemon();
  }, []);

  const value = {
    allPokemon,
    loading,
    error
  };

  return (
    <PokemonContext.Provider value={value}>
      {children}
    </PokemonContext.Provider>
  );
}

// Custom hook to use Pokemon data
export function usePokemonData() {
  const context = useContext(PokemonContext);
  if (!context) {
    throw new Error('usePokemonData must be used within a PokemonProvider');
  }
  return context;
}
