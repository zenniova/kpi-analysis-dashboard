import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataVisualization from './components/DataVisualization';
import Report from './components/Report';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Data Visualizer</h1>
        <p>Upload your CSV file to visualize your data</p>
      </header>

      <main>
        <FileUpload 
          onDataReceived={setData} 
          onError={setError}
        />
        
        {error && (
          <div className="error-message">
            <i className="fas fa-exclamation-circle"></i>
            <span>{error}</span>
          </div>
        )}

        {!data && !error && (
          <div className="welcome-section">
            <div className="features">
              <div className="feature-card">
                <i className="fas fa-chart-line"></i>
                <h3>Line Charts</h3>
                <p>Visualize trends in your numerical data</p>
              </div>
              <div className="feature-card">
                <i className="fas fa-table"></i>
                <h3>Data Preview</h3>
                <p>Quick look at your data structure</p>
              </div>
              <div className="feature-card">
                <i className="fas fa-chart-scatter"></i>
                <h3>Scatter Plots</h3>
                <p>Explore relationships between variables</p>
              </div>
            </div>
          </div>
        )}

        {data && (
          <div className="data-section">
            <Report data={data} />
            <DataVisualization data={data} />
          </div>
        )}
      </main>

      <footer className="App-footer">
        <span className="developer-credit">developed by Zenni</span>
      </footer>
    </div>
  );
}

export default App; 