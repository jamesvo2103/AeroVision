import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import Hero from './components/Hero/Hero';
import SimulationUpload from './components/SimulationUpload/SimulationUpload';
import Overview from './components/Overview/Overview'; // Import your Overview page

function App() {
  return (
    <Router>
      <div className="hero-container">
        <Header />
        <Routes>
          <Route path="/" element={<Hero />} />
          <Route path="/upload" element={<SimulationUpload />} />
          <Route path="/overview" element={<Overview />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
