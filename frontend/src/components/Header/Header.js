import React from 'react';

const logoUrl = "https://innovationspace.ansys.com/wp-content/uploads/2024/08/Airfoil-Geometry-and-Aerodynamics.png";

// Header component: displays logo and navigation links
function Header({ onLogoClick }) {
  return (
    <header className="hero-header">
      {/* Logo is now clickable */}
      <img
        src={logoUrl}
        alt="AeroVision Logo"
        className="hero-logo"
        style={{ cursor: 'pointer' }}
        onClick={onLogoClick}
      />
      <nav className="hero-nav">
        <a href="#product">Product</a>
        <a href="#solutions">Solutions</a>
        <a href="#resources">Resources</a>
        <a href="#pricing">Pricing</a>
        <button className="login-btn">Log In</button>
        <button className="signup-btn">Sign Up</button>
      </nav>
    </header>
  );
}

export default Header;