import React, { useState } from 'react';
import './SimulationUpload.css';

// SimulationUpload component: form for uploading 3D model and selecting simulation options
function SimulationUpload() {
  // State for file, simulation goal, and simulation name
  const [file, setFile] = useState(null);
  const [angle, setAngle] = useState('');
  const [loading, setLoading] = useState(false);
  const [resultUrl, setResultUrl] = useState(null);
  const [inputUrl, setInputUrl] = useState(null);
  const [error, setError] = useState('');

  // Handle file input change
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handle file drop in the drop zone
  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  // Handle drag over event for the drop zone
  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleAngleChange = (e) => {
    setAngle(e.target.value);
  };

  // Submit form data to backend and show the generated airflow image
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !angle) {
      alert('Please select a file and angle of attack.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('angle_of_attack', angle);

    setLoading(true);
    setError('');
    setResultUrl(null);
    setInputUrl(URL.createObjectURL(file));

    try {
      const response = await fetch('http://localhost:8000/predict-airflow/', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }
      const blob = await response.blob();
      setResultUrl(URL.createObjectURL(blob));
    } catch (err) {
      setError('Prediction failed. Is the backend running on port 8000?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="sim-upload-page">
      {/* Guidelines card */}
      <div className="sim-guidelines-card">
        <h3>Simulation <span className="sim-guidelines-bold">Guidelines</span></h3>
        <ul>
          <li>File formats: <b>.stl</b> (.png, .jpg also supported)</li>
          <li>Don't have your airfoil? Get one from UIUC database</li>
        </ul>
      </div>
      {/* Upload form */}
      <form className="sim-upload-form" onSubmit={handleSubmit}>
        {/* File upload drop zone */}
        <div
          className="sim-dropzone"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="sim-dropzone-content">
            <div className="sim-dropzone-icon">☁️</div>
            <div>
              <b>DRAG & DROP</b>
              <div className="sim-dropzone-browse">
                Your 3D file here, <label htmlFor="file-upload" className="sim-browse-link">browse</label>
              </div>
            </div>
          </div>
          <input
            id="file-upload"
            type="file"
            accept=".stl,.obj,.step,.stp,.iges,.igs,.png,.jpg,.jpeg"
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </div>
        {/* Display uploaded file name */}
        {file && (
          <div className="sim-upload-success">
            <span className="sim-upload-success-icon">✅</span> {file.name}
          </div>
        )}
        {/* Angle of attack dropdown */}
        <div className="sim-upload-field">
          <label htmlFor="angle-select">Angle of Attack:&nbsp;</label>
          <select
            id="angle-select"
            value={angle}
            onChange={handleAngleChange}
            required
          >
            <option value="">Select angle</option>
            <option value="0">0°</option>
            <option value="25">25°</option>
            <option value="50">50°</option>
          </select>
        </div>
        {/* External link button and submit */}
        <div className="sim-upload-actions">
          <a
            href="https://dat-to-stl-app-f7grcfg8hfcnujte8rglnn.streamlit.app/"
            target="_blank"
            rel="noopener noreferrer"
            className="external-link-btn"
          >
            Get your own Airfoil
          </a>
          <button type="submit" className="sim-submit-btn" disabled={loading}>
            {loading ? 'Generating…' : 'Submit'}
          </button>
        </div>
      </form>

      {/* Results */}
      {error && <div className="sim-upload-error">{error}</div>}
      {(inputUrl || resultUrl) && (
        <div className="sim-results">
          {inputUrl && (
            <figure className="sim-result-item">
              <img src={inputUrl} alt="Input airfoil" />
              <figcaption>Input airfoil</figcaption>
            </figure>
          )}
          <figure className="sim-result-item">
            {loading ? (
              <div className="sim-result-loading">Generating airflow…</div>
            ) : (
              resultUrl && <img src={resultUrl} alt="Airflow output" />
            )}
            <figcaption>Airflow (AoA {angle}°)</figcaption>
          </figure>
        </div>
      )}
    </div>
  );
}

export default SimulationUpload;