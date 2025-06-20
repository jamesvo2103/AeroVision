import React from 'react';
import { Link } from 'react-router-dom';
const logoUrl = "aerovision_logo.png"; // Replace with your actual logo URL

// Header component: displays logo and navigation links
function Header() {
  return (
    <header className="hero-header">
      {/* Logo links to home page */}
      <Link to="/">
        <img
          src={logoUrl}
          alt="AeroVision Logo"
          className="hero-logo"
          style={{ cursor: 'pointer' }}
        />
      </Link>
      <nav className="hero-nav">
        <Link to="/">Home</Link>
        <Link to="/overview">Overview</Link>
        <Link to="/upload">Simulate</Link>
        {/* Add more links as needed */}
      </nav>
    </header>
  );
}

export default Header;