// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { PokemonProvider } from './contexts/PokemonContext.jsx';
import Home from './components/Home.jsx';
import Search from './components/Search.jsx';
import Battle from './components/Battle.jsx';
import Skills from './components/Skills.jsx';
import Rankings from './components/Rankings.jsx';
import './styles.css';

function App() {
  return (
    <PokemonProvider>
      <Router>
        <div className="app-container">
          <nav className="nav">
            <div className="nav-links">
              <Link to="/" className="nav-link">🏠 Home</Link>
              <Link to="/search" className="nav-link">🔍 Search Pokémon</Link>
              <Link to="/battle" className="nav-link">⚔️ Battle Simulator</Link>
              <Link to="/skills" className="nav-link">🎯 Skills & Moves</Link>
              <Link to="/rankings" className="nav-link">📈 Rankings</Link>
            </div>
          </nav>

          <div className="page-container">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/search" element={<Search />} />
              <Route path="/battle" element={<Battle />} />
              <Route path="/skills" element={<Skills />} />
              <Route path="/rankings" element={<Rankings />} />
            </Routes>
          </div>
        </div>
      </Router>
    </PokemonProvider>
  );
}

export default App;
