// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './components/Home.jsx';
import Search from './components/Search.jsx';
import Battle from './components/Battle.jsx';
import Rankings from './components/Rankings.jsx';
import './styles.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <nav className="nav">
          <div className="nav-links">
            <Link to="/" className="nav-link">🏠 Home</Link>
            <Link to="/search" className="nav-link">🔍 Search Pokémon</Link>
            <Link to="/rankings" className="nav-link">📈 Rankings</Link>
            <Link to="/battle" className="nav-link">⚔️ Battle Simulator</Link>
          </div>
        </nav>

        <div className="page-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<Search />} />
            <Route path="/rankings" element={<Rankings />} />
            <Route path="/battle" element={<Battle />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
