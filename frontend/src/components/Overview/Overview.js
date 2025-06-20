import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Overview.css';

function Overview() {
  const navigate = useNavigate();

  const handleStartSimulating = () => {
    navigate('/upload');
  };

  return (
    <div className="overview-container">
      {/* Top half: summary and images side by side */}
      <div className="overview-top">
        <div className="summary">
          <h1 className="overview-title">
            An affordable, intuitive tools to visualize airflow around airfoils.
          </h1>
          <div className="overview-actions">
            <button
              className="overview-btn primary"
              onClick={handleStartSimulating}
            >
              Start Simulating Now
            </button>
          </div>
        </div>
        <div className="overview-visual">
          <img
            src="https://fsp.norasci.com/tutorials/windtunnel_airfoil/images/inst_res.png"
            alt="Simulation Example"
            className="overview-main-img"
          />
          <img
            src="https://arc.osu.edu/sites/default/files/styles/coe_large/public/media/figure_1_airfoil.jpg?itok=lS-hm-wo"
            alt="Wind Tunnel Experiment"
            className="overview-main-img"
          />
        </div>
      </div>

      {/* Feature Section */}
      <h2 className="feature-section-title">Why AeroVision</h2>
      <div className="feature-section">
        {/* Feature 1 & 2 Combined - image on the right */}
        <div className="feature-row reverse">
          <img
            src="https://media.springernature.com/lw685/springer-static/image/art%3A10.1038%2Fs41598-025-95848-4/MediaObjects/41598_2025_95848_Fig9_HTML.png"
            alt="Accessible & Accuracy"
            className="feature-img"
          />
          <div className="feature-text">
            <h2 className="feature-title">Accessible & Easy to use</h2>
            <p className="feature-desc">
              Accepts common inputs: airfoil image or STL file.
              <br />
              Predictions available across various angles of attack.
              <br />
              No hardware, local installation needed.
            </p>
            <h2 className="feature-title" style={{ marginTop: '32px' }}>
              Accuracy
            </h2>
            <p className="feature-desc">
              AeroVision’s AI tools accelerate predictions so results arrive at
              the speed of thought.
              <br />
              ≥ 85% qualitative agreement with actual string motion patterns in
              test cases.
            </p>
          </div>
        </div>
        {/* Feature 3 & 4 Combined - image on the left */}
        <div className="feature-row">
          <img
            src="value.jpg"
            alt="Affordable and Educational Value"
            className="feature-img"
          />
          <div className="feature-text">
            <h2 className="feature-title">Affordable</h2>
            <p className="feature-desc">
              Designed for students, hobbyists, and educators without access to
              professional CFD tools or wind tunnels who want a superficial
              insight into a certain design before moving on to a more expensive
              and sophisticated method.
            </p>
            <h2 className="feature-title" style={{ marginTop: '32px' }}>
              Educational Value
            </h2>
            <p className="feature-desc">
              Qualitative visualizations clearly illustrating aerodynamic concepts
              such as flow separation zones, turbulence and wake regions, vortices
              and attachment points.
              <br />
              Excellent tool for visually teaching aerodynamic fundamentals:
              Bernoulli’s principle (lift & drag), stall behavior and boundary
              layer dynamics.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Overview;