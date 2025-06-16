import './App.css';
import React, { Component } from 'react';
import Header from './components/Header/Header';
import Hero from './components/Hero/Hero';
import SimulationUpload from './components/SimulationUpload/SimulationUpload';

// Main App component controlling page navigation
class App extends Component {
  state = {
    page: 'home'
  };

  // Handler to switch to the upload page
  handleStartSimulating = () => {
    this.setState({ page: 'upload' });
  };

  // Handler to switch to the home page
  handleGoHome = () => {
    this.setState({ page: 'home' });
  };

  render() {
    return (
      <div className="hero-container">
        <Header onLogoClick={this.handleGoHome} /> {/* Pass handler to Header */}
        {this.state.page === 'home' ? (
          <Hero onStart={this.handleStartSimulating} />
        ) : (
          <SimulationUpload />
        )}
      </div>
    );
  }
}

export default App;
