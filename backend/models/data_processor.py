import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import logging
import numpy as np

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, before_df: pd.DataFrame, after_df: pd.DataFrame, data_type: str = 'daily'):
        try:
            self.before_df = before_df.copy()
            self.after_df = after_df.copy()
            self.data_type = data_type
            
            # Standardisasi nama kolom
            self.before_df.columns = [col.upper() for col in self.before_df.columns]
            self.after_df.columns = [col.upper() for col in self.after_df.columns]
            
            # Konversi kolom waktu berdasarkan tipe data
            for df in [self.before_df, self.after_df]:
                if self.data_type == 'hourly':
                    if 'DATE' in df.columns and 'HOUR' in df.columns:
                        # Coba beberapa format tanggal yang umum
                        try:
                            # Format MM/DD/YYYY
                            df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y')
                        except:
                            try:
                                # Format YYYY-MM-DD
                                df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')
                            except:
                                # Format lainnya, biarkan pandas mendeteksi
                                df['DATE'] = pd.to_datetime(df['DATE'])
                        
                        # Konversi jam ke format yang benar
                        df['HOUR'] = df['HOUR'].astype(str).str.zfill(2) + ':00'
                        
                        # Gabungkan DATE dan HOUR
                        df['DATETIME'] = pd.to_datetime(
                            df['DATE'].dt.strftime('%Y-%m-%d') + ' ' + df['HOUR']
                        )
                else:  # daily
                    if 'DATE' in df.columns:
                        try:
                            # Format MM/DD/YYYY
                            df['DATE'] = pd.to_datetime(df['DATE'], format='%m/%d/%Y')
                        except:
                            try:
                                # Format YYYY-MM-DD
                                df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')
                            except:
                                # Format lainnya, biarkan pandas mendeteksi
                                df['DATE'] = pd.to_datetime(df['DATE'])
            
            # Handle missing values
            self.before_df = self.before_df.replace([np.inf, -np.inf], np.nan).fillna(0)
            self.after_df = self.after_df.replace([np.inf, -np.inf], np.nan).fillna(0)
            
            logger.info(f"Data loaded with columns: {list(self.before_df.columns)}")
            logger.info(f"Date range before: {self.before_df['DATE'].min()} to {self.before_df['DATE'].max()}")
            logger.info(f"Date range after: {self.after_df['DATE'].min()} to {self.after_df['DATE'].max()}")
        except Exception as e:
            logger.error(f"Error initializing DataProcessor: {str(e)}")
            raise

    def calculate_kpi_changes(self):
        """Hitung perubahan KPI antara data before dan after"""
        try:
            kpi_metrics = {
                'PAYLOAD_GB': {'name': 'Total Payload (GB)', 'threshold': 5, 'better': 'higher'},
                'PRB_DL_UTIL': {'name': 'DL PRB Utilization (%)', 'threshold': 2, 'better': 'lower'},
                'USER_DL_THROUGHPUT': {'name': 'User DL Throughput (Mbps)', 'threshold': 5, 'better': 'higher'},
                'TOTAL_USER': {'name': 'Total User Number', 'threshold': 5, 'better': 'higher'},
                'ACTIVE_USER': {'name': 'Active User', 'threshold': 5, 'better': 'higher'},
                'CQI': {'name': 'CQI Average', 'threshold': 1, 'better': 'higher'},
                'CEU_RATIO': {'name': 'CEU Ratio (%)', 'threshold': 2, 'better': 'lower'},
                'MR_LESS_105DBM': {'name': 'MR Less than -105dBm', 'threshold': 2, 'better': 'lower'}
            }

            results = []
            for metric, info in kpi_metrics.items():
                if metric in self.before_df.columns and metric in self.after_df.columns:
                    # Hitung rata-rata berdasarkan tipe data
                    if self.data_type == 'hourly':
                        before_value = self.before_df.groupby('DATE')[metric].mean().mean()
                        after_value = self.after_df.groupby('DATE')[metric].mean().mean()
                    else:
                        before_value = self.before_df[metric].mean()
                        after_value = self.after_df[metric].mean()
                    
                    if before_value == 0:
                        pct_change = 0
                    else:
                        pct_change = ((after_value - before_value) / before_value) * 100
                    
                    if abs(pct_change) <= info['threshold']:
                        status = 'Maintain'
                    else:
                        is_improvement = (pct_change > 0) == (info['better'] == 'higher')
                        status = 'Improve' if is_improvement else 'Degrade'

                    results.append({
                        'metric': info['name'],
                        'before': round(before_value, 2),
                        'after': round(after_value, 2),
                        'delta': round(after_value - before_value, 2),
                        'percentage': round(pct_change, 2),
                        'status': status,
                        'threshold': info['threshold']
                    })

            return results
        except Exception as e:
            logger.error(f"Error calculating KPI changes: {str(e)}")
            raise

    def get_data_stats(self, compare_date=None) -> dict:
        """Generate KPI statistics"""
        try:
            kpi_changes = self.calculate_kpi_changes()
            return {
                "total_rows": len(self.before_df),
                "data": kpi_changes,
                "date_range": {
                    "start": self.before_df['DATE'].min().strftime('%Y-%m-%d'),
                    "end": self.before_df['DATE'].max().strftime('%Y-%m-%d'),
                    "compare": compare_date or self.before_df['DATE'].min().strftime('%Y-%m-%d')
                },
                "metrics": [
                    'PAYLOAD_GB', 'TOTAL_USER', 'USER_DL_THROUGHPUT',
                    'PRB_DL_UTIL', 'CQI', 'ACTIVE_USER'
                ]
            }
        except Exception as e:
            logger.error(f"Error generating stats: {str(e)}")
            raise

    def generate_plots(self) -> dict:
        """Generate KPI visualizations dengan before-after comparison"""
        try:
            plots = {}
            plt.style.use('default')
            
            # Konfigurasi plot
            plt.rcParams.update({
                'figure.figsize': (12, 6),
                'axes.grid': True,
                'grid.alpha': 0.3,
                'font.size': 10
            })

            main_metrics = [
                'PAYLOAD_GB', 'TOTAL_USER', 'USER_DL_THROUGHPUT',
                'PRB_DL_UTIL', 'CQI', 'ACTIVE_USER'
            ]

            for metric in main_metrics:
                if metric in self.before_df.columns and metric in self.after_df.columns:
                    plt.figure()
                    
                    if self.data_type == 'hourly':
                        # Untuk data hourly, gunakan datetime dan format jam
                        before_data = self.before_df.copy()
                        after_data = self.after_df.copy()
                        
                        # Format x-axis untuk hourly
                        plt.plot(before_data['DATETIME'], before_data[metric],
                                marker='o', markersize=3, linewidth=1.5,
                                color='#1976D2', alpha=0.7, label='Before')
                        plt.plot(after_data['DATETIME'], after_data[metric],
                                marker='o', markersize=3, linewidth=1.5,
                                color='#4CAF50', alpha=0.7, label='After')
                        
                        # Format x-axis
                        plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
                        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d %H:00'))
                        
                    else:  # daily
                        # Untuk data daily, gunakan date saja
                        plt.plot(self.before_df['DATE'], self.before_df[metric],
                                marker='o', markersize=4, linewidth=1.5,
                                color='#1976D2', alpha=0.7, label='Before')
                        plt.plot(self.after_df['DATE'], self.after_df[metric],
                                marker='o', markersize=4, linewidth=1.5,
                                color='#4CAF50', alpha=0.7, label='After')
                        
                        # Format x-axis
                        plt.gcf().autofmt_xdate()
                        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))

                    # Hitung statistik
                    if self.data_type == 'hourly':
                        before_avg = self.before_df.groupby('DATE')[metric].mean().mean()
                        after_avg = self.after_df.groupby('DATE')[metric].mean().mean()
                    else:
                        before_avg = self.before_df[metric].mean()
                        after_avg = self.after_df[metric].mean()
                    
                    pct_change = ((after_avg - before_avg) / before_avg) * 100

                    # Tambahkan statistik ke judul
                    plt.title(f'{metric}\nBefore Avg: {before_avg:.2f}, After Avg: {after_avg:.2f}\nChange: {pct_change:+.2f}%')
                    
                    # Styling
                    plt.xlabel('Time' if self.data_type == 'hourly' else 'Date')
                    plt.ylabel(metric)
                    plt.legend()
                    plt.grid(True, alpha=0.3)
                    
                    # Sesuaikan margin
                    plt.tight_layout()
                    
                    # Save plot
                    buf = BytesIO()
                    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                    plt.close()
                    buf.seek(0)
                    plots[metric] = base64.b64encode(buf.read()).decode('utf-8')

            return plots
            
        except Exception as e:
            logger.error(f"Error generating plots: {str(e)}")
            raise 