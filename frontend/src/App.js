import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Analytics from './pages/Analytics';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-brand">
            <Link to="/">Coffee Grinder Bot</Link>
          </div>
          <ul className="nav-links">
            <li><Link to="/">Главная</Link></li>
            <li><Link to="/analytics">Аналитика</Link></li>
          </ul>
        </nav>

        <main className="container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>&copy; 2024 Coffee Grinder Bot. Все права защищены.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App; 