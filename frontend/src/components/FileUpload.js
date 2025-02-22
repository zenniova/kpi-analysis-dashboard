import React, { useState, useRef } from 'react';
import './FileUpload.css';

function FileUpload({ onDataReceived, onError }) {
  const [loading, setLoading] = useState(false);
  const [beforeFile, setBeforeFile] = useState(null);
  const [afterFile, setAfterFile] = useState(null);
  const [draggingBefore, setDraggingBefore] = useState(false);
  const [draggingAfter, setDraggingAfter] = useState(false);
  const [dataType, setDataType] = useState('daily');
  const beforeFileRef = useRef(null);
  const afterFileRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragIn = (e, type) => {
    e.preventDefault();
    e.stopPropagation();
    if (type === 'before') {
      setDraggingBefore(true);
    } else {
      setDraggingAfter(true);
    }
  };

  const handleDragOut = (e, type) => {
    e.preventDefault();
    e.stopPropagation();
    if (type === 'before') {
      setDraggingBefore(false);
    } else {
      setDraggingAfter(false);
    }
  };

  const handleDrop = (e, type) => {
    e.preventDefault();
    e.stopPropagation();
    if (type === 'before') {
      setDraggingBefore(false);
    } else {
      setDraggingAfter(false);
    }

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (!file.name.endsWith('.csv')) {
        onError('Please upload CSV files only');
        return;
      }
      if (type === 'before') {
        setBeforeFile(file);
      } else {
        setAfterFile(file);
      }
    }
  };

  const handleFileSelect = (event, type) => {
    const file = event.target.files[0];
    if (file) {
      if (!file.name.endsWith('.csv')) {
        onError('Please upload CSV files only');
        return;
      }
      if (type === 'before') {
        setBeforeFile(file);
      } else {
        setAfterFile(file);
      }
    }
  };

  const processFiles = async () => {
    if (!beforeFile || !afterFile) {
      onError('Please upload both before and after files');
      return;
    }

    const formData = new FormData();
    formData.append('before_file', beforeFile);
    formData.append('after_file', afterFile);
    formData.append('data_type', dataType);

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }
      
      const data = await response.json();
      onDataReceived(data);
      onError(null);
    } catch (error) {
      console.error('Error uploading files:', error);
      onError(error.message);
      onDataReceived(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <div className="data-type-selector">
        <h3>Select Data Type</h3>
        <div className="radio-group">
          <label>
            <input
              type="radio"
              value="daily"
              checked={dataType === 'daily'}
              onChange={(e) => setDataType(e.target.value)}
            />
            Daily Data
          </label>
          <label>
            <input
              type="radio"
              value="hourly"
              checked={dataType === 'hourly'}
              onChange={(e) => setDataType(e.target.value)}
            />
            Hourly Data
          </label>
        </div>
      </div>

      <div className="upload-boxes">
        <div className="upload-box">
          <h3>Before Implementation</h3>
          <div 
            className={`upload-zone ${draggingBefore ? 'dragging' : ''}`}
            onClick={() => beforeFileRef.current.click()}
            onDragEnter={(e) => handleDragIn(e, 'before')}
            onDragLeave={(e) => handleDragOut(e, 'before')}
            onDragOver={handleDrag}
            onDrop={(e) => handleDrop(e, 'before')}
          >
            <i className="fas fa-cloud-upload-alt upload-icon"></i>
            <p className="upload-text">
              Drag and drop before data CSV file here<br />
              or click to browse
            </p>
            <input
              ref={beforeFileRef}
              type="file"
              accept=".csv"
              onChange={(e) => handleFileSelect(e, 'before')}
              style={{ display: 'none' }}
            />
          </div>
          {beforeFile && (
            <div className="file-info">
              <i className="fas fa-file-csv"></i>
              <span>{beforeFile.name}</span>
              <button 
                className="remove-file"
                onClick={() => setBeforeFile(null)}
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
          )}
        </div>

        <div className="upload-box">
          <h3>After Implementation</h3>
          <div 
            className={`upload-zone ${draggingAfter ? 'dragging' : ''}`}
            onClick={() => afterFileRef.current.click()}
            onDragEnter={(e) => handleDragIn(e, 'after')}
            onDragLeave={(e) => handleDragOut(e, 'after')}
            onDragOver={handleDrag}
            onDrop={(e) => handleDrop(e, 'after')}
          >
            <i className="fas fa-cloud-upload-alt upload-icon"></i>
            <p className="upload-text">
              Drag and drop after data CSV file here<br />
              or click to browse
            </p>
            <input
              ref={afterFileRef}
              type="file"
              accept=".csv"
              onChange={(e) => handleFileSelect(e, 'after')}
              style={{ display: 'none' }}
            />
          </div>
          {afterFile && (
            <div className="file-info">
              <i className="fas fa-file-csv"></i>
              <span>{afterFile.name}</span>
              <button 
                className="remove-file"
                onClick={() => setAfterFile(null)}
              >
                <i className="fas fa-times"></i>
              </button>
            </div>
          )}
        </div>
      </div>

      <button 
        className="compare-button"
        onClick={processFiles}
        disabled={!beforeFile || !afterFile || loading}
      >
        {loading ? (
          <>
            <i className="fas fa-spinner fa-spin"></i>
            Processing...
          </>
        ) : (
          'Compare Data'
        )}
      </button>
    </div>
  );
}

export default FileUpload; 