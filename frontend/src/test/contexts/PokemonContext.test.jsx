import React from 'react'
import { renderHook, waitFor } from '@testing-library/react'
import { PokemonProvider, usePokemonData } from '../../../contexts/PokemonContext'
import { mockFetch, mockFetchError, mockApiResponses } from '../utils'

describe('PokemonContext', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('PokemonProvider', () => {
    it('should provide initial loading state', () => {
      mockFetch(mockApiResponses.getAllPokemon)
      
      const wrapper = ({ children }) => (
        <PokemonProvider>{children}</PokemonProvider>
      )
      
      const { result } = renderHook(() => usePokemonData(), { wrapper })
      
      expect(result.current.loading).toBe(true)
      expect(result.current.allPokemon).toEqual([])
      expect(result.current.error).toBe(null)
    })

    it('should load Pokemon data successfully', async () => {
      mockFetch(mockApiResponses.getAllPokemon)
      
      const wrapper = ({ children }) => (
        <PokemonProvider>{children}</PokemonProvider>
      )
      
      const { result } = renderHook(() => usePokemonData(), { wrapper })
      
      await waitFor(() => {
        expect(result.current.loading).toBe(false)
      })
      
      expect(result.current.allPokemon).toEqual(mockApiResponses.getAllPokemon.results)
      expect(result.current.error).toBe(null)
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/pokemon/?limit=1000')
    })

    it('should handle API errors gracefully', async () => {
      mockFetchError(new Error('Network error'))
      
      const wrapper = ({ children }) => (
        <PokemonProvider>{children}</PokemonProvider>
      )
      
      const { result } = renderHook(() => usePokemonData(), { wrapper })
      
      await waitFor(() => {
        expect(result.current.loading).toBe(false)
      })
      
      expect(result.current.allPokemon).toEqual([])
      expect(result.current.error).toBe('Network error')
    })

    it('should handle HTTP errors', async () => {
      mockFetch({}, false, 500)
      
      const wrapper = ({ children }) => (
        <PokemonProvider>{children}</PokemonProvider>
      )
      
      const { result } = renderHook(() => usePokemonData(), { wrapper })
      
      await waitFor(() => {
        expect(result.current.loading).toBe(false)
      })
      
      expect(result.current.allPokemon).toEqual([])
      expect(result.current.error).toBe('HTTP error! status: 500')
    })
  })

  describe('usePokemonData', () => {
    it('should throw error when used outside provider', () => {
      // Suppress console.error for this test
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
      
      expect(() => {
        renderHook(() => usePokemonData())
      }).toThrow('usePokemonData must be used within a PokemonProvider')
      
      consoleSpy.mockRestore()
    })

    it('should return context value when used within provider', () => {
      mockFetch(mockApiResponses.getAllPokemon)
      
      const wrapper = ({ children }) => (
        <PokemonProvider>{children}</PokemonProvider>
      )
      
      const { result } = renderHook(() => usePokemonData(), { wrapper })
      
      expect(result.current).toHaveProperty('allPokemon')
      expect(result.current).toHaveProperty('loading')
      expect(result.current).toHaveProperty('error')
    })
  })
})
