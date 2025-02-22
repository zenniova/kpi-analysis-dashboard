import React from 'react';
import './DataVisualization.css';

function DataVisualization({ data }) {
  if (!data?.visualizations) return null;

  // Definisikan metrics yang akan ditampilkan
  const metrics = [
    'PAYLOAD_GB', 'TOTAL_USER', 'USER_DL_THROUGHPUT',
    'PRB_DL_UTIL', 'CQI', 'ACTIVE_USER'
  ];

  return (
    <div className="visualizations">
      <h2>KPI Visualizations</h2>
      
      <div className="plots-grid">
        {metrics.map(metric => {
          if (data.visualizations[metric]) {
            return (
              <div key={metric} className="plot-container">
                <h3>{metric.replace(/_/g, ' ')}</h3>
                <img 
                  src={`data:image/png;base64,${data.visualizations[metric]}`}
                  alt={`Plot of ${metric}`}
                  className="plot-image"
                />
              </div>
            );
          }
          return null;
        })}
      </div>
    </div>
  );
}

export default DataVisualization; 