import React from 'react';
import './Report.css';

function Report({ data }) {
  if (!data?.statistics?.data) return null;

  const { data: metrics } = data.statistics;

  return (
    <div className="report">
      <h2>KPI Analysis Report</h2>
      <div className="data-table">
        <table>
          <thead>
            <tr>
              <th>Metric</th>
              <th>Before</th>
              <th>After</th>
              <th>Change (%)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {metrics.map((row, index) => (
              <tr key={index}>
                <td>{row.metric}</td>
                <td>{row.before.toFixed(2)}</td>
                <td>{row.after.toFixed(2)}</td>
                <td className={row.percentage >= 0 ? 'positive' : 'negative'}>
                  {row.percentage >= 0 ? '+' : ''}{row.percentage.toFixed(2)}%
                </td>
                <td className={`status ${row.status.toLowerCase()}`}>
                  {row.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Report; 