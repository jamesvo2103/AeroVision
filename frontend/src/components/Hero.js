import React from 'react';

function Hero({ onStart }) {
  return (
    <main className="hero-main">
      <div className="hero-text">
        <h1>Physics & AI engineering simulation in the cloud</h1>
        <p>
          AeroVision empowers engineers to innovate faster with airflow simulation.
        </p>
        <button className="cta-btn" onClick={onStart}>Start Simulating Now</button>
      </div>
      <div className="hero-image">
        <img
          src="https://innovationspace.ansys.com/wp-content/uploads/2024/08/Airfoil-Geometry-and-Aerodynamics.png"
          alt="Simulation Example"
        />
      </div>
    </main>
  );
}

export default Hero;