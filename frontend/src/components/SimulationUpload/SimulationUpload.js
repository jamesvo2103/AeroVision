import React, { useState } from 'react';

// SimulationUpload component: form for uploading image and selecting angle
function SimulationUpload() {
  // State for file, angle, and image preview
  const [file, setFile] = useState(null);
  const [angle, setAngle] = useState('');
  const [preview, setPreview] = useState(null);

  // Handle file input change and set preview
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    if (selectedFile) {
      setPreview(URL.createObjectURL(selectedFile));
    } else {
      setPreview(null);
    }
  };

  // Handle dropdown change
  const handleAngleChange = (e) => {
    setAngle(e.target.value);
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`File: ${file ? file.name : 'None'}, Angle: ${angle}`);
  };

  return (
    <div className="upload-container">
      {/* Upload form */}
      <form onSubmit={handleSubmit} className="upload-form">
        {/* File input and angle dropdown */}
        <input type="file" accept="image/*" onChange={handleFileChange} required />
        <br /><br />
        <label>
          Angle of Attack:&nbsp;
          <select value={angle} onChange={handleAngleChange} required>
            <option value="">Select angle</option>
            <option value="0">0°</option>
            <option value="5">5°</option>
            <option value="10">10°</option>
            <option value="15">15°</option>
            <option value="20">20°</option>
          </select>
        </label>
        <br /><br />
        <button type="submit">Submit</button>
      </form>
      {/* Image preview if file is selected */}
      {preview && (
        <div className="upload-image-preview">
          <img src={preview} alt="Preview" />
        </div>
      )}
    </div>
  );
}

export default SimulationUpload;