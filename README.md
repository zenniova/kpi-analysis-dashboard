# KPI Analysis Dashboard

A web application for analyzing and visualizing KPI (Key Performance Indicator) data, comparing before and after implementation metrics for network performance analysis.

## Features

- **Data Upload**
  - Support for both daily and hourly data formats
  - Drag & drop interface for CSV files
  - Before/After implementation comparison
  - CSV validation and error handling

- **KPI Analysis**
  - Automatic calculation of KPI changes
  - Status determination (Improve/Degrade/Maintain)
  - Threshold-based evaluation
  - Daily/Hourly data aggregation

- **Visualizations**
  - Interactive time series plots
  - Before vs After comparison charts
  - Customized date/time formatting
  - Responsive design

## Supported KPI Metrics

- Payload (GB)
- PRB DL Utilization (%)
- User DL Throughput (Mbps)
- Total User Count
- Active Users
- CQI Average
- CEU Ratio (%)
- MR Less than -105dBm

## Tech Stack

### Frontend
- React.js
- Modern CSS3 (Flexbox/Grid)
- Font Awesome Icons
- Chart visualization libraries

### Backend
- FastAPI
- Pandas for data processing
- Matplotlib for plotting
- NumPy for calculations

## Project Structure
