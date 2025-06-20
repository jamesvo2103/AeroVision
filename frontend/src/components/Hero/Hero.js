import React from 'react';
import { useNavigate } from 'react-router-dom';

function Hero() {
  const navigate = useNavigate();

  return (
    <main className="hero-main">
      <div className="hero-text">
        <h1>Physics & AI engineering simulation in the cloud</h1>
        <p>
          AeroVision empowers engineers to innovate faster with airflow simulation.
        </p>
        <button className="cta-btn" onClick={() => navigate('/upload')}>Start Simulating Now</button>
      </div>
      <div className="hero-image">
        <img
          src="GIF-2.gif"
          alt="Moving Smoke Airfoil"
          className="smoke-gif"
          style={{ width: '100%', maxWidth: '1000px', borderRadius: '16px' }}
        />
      </div>
    </main>
  );
}

export default Hero;