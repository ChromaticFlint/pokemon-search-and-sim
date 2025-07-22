import React from 'react'
import { render } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { PokemonProvider } from '../../contexts/PokemonContext'

// Custom render function that includes providers
export function renderWithProviders(ui, options = {}) {
  const { initialEntries = ['/'], ...renderOptions } = options

  function Wrapper({ children }) {
    return (
      <BrowserRouter>
        <PokemonProvider>
          {children}
        </PokemonProvider>
      </BrowserRouter>
    )
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions })
}

// Mock Pokemon data for testing
export const mockPokemonData = [
  {
    id: 25,
    name: "Pikachu",
    metadata: {
      stats: {
        hp: 35,
        attack: 55,
        defense: 40,
        special_attack: 50,
        special_defense: 50,
        speed: 90
      },
      sprite_url: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
      types: ["electric"]
    }
  },
  {
    id: 6,
    name: "Charizard",
    metadata: {
      stats: {
        hp: 78,
        attack: 84,
        defense: 78,
        special_attack: 109,
        special_defense: 85,
        speed: 100
      },
      sprite_url: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
      types: ["fire", "flying"]
    }
  },
  {
    id: 150,
    name: "Mewtwo",
    metadata: {
      stats: {
        hp: 106,
        attack: 110,
        defense: 90,
        special_attack: 154,
        special_defense: 90,
        speed: 130
      },
      sprite_url: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png",
      types: ["psychic"]
    }
  }
]

// Mock API responses
export const mockApiResponses = {
  searchSimilar: {
    results: [
      {
        id: 25,
        name: "Pikachu",
        score: 0.95,
        distance: 0.05,
        metadata: mockPokemonData[0].metadata
      }
    ]
  },
  searchByName: {
    results: [mockPokemonData[0]]
  },
  getAllPokemon: {
    results: mockPokemonData
  },
  getTopPokemon: {
    results: [mockPokemonData[2], mockPokemonData[1], mockPokemonData[0]],
    criteria: "power"
  },
  battleSimple: {
    result: "Pokemon A wins"
  },
  battleAdvanced: {
    result: "Charizard wins!",
    battle_log: [
      "--- Turn 1 ---",
      "Charizard used Flamethrower!",
      "It's super effective!",
      "Pikachu fainted!",
      "🏆 Charizard wins the battle!"
    ],
    final_hp: { pokemon_a: 0, pokemon_b: 45 },
    turns: 1
  }
}

// Helper to mock fetch responses
export function mockFetch(response, ok = true, status = 200) {
  fetch.mockResolvedValueOnce({
    ok,
    status,
    json: async () => response,
  })
}

// Helper to mock fetch errors
export function mockFetchError(error = new Error('Network error')) {
  fetch.mockRejectedValueOnce(error)
}

// Helper to wait for async operations
export const waitFor = (ms) => new Promise(resolve => setTimeout(resolve, ms))

// Re-export everything from testing-library
export * from '@testing-library/react'
export { default as userEvent } from '@testing-library/user-event'
