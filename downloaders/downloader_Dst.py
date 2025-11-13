import pyspedas
import pandas as pd
from pytplot import get_data

#----------------------------------------------------------------------------
# Configuration
start_date = '1995-01-01'
end_date = '2024-12-31'
range_date = [start_date, end_date]

print(f"Processing Dst data from {start_date} to {end_date}...")

#----------------------------------------------------------------------------
# Download Dst data
# Check https://pyspedas.readthedocs.io/en/latest/kyoto.html

print("Downloading Dst data...")

try:
    dst_vars = pyspedas.projects.kyoto.dst(trange=range_date)
except Exception as e:
    print(f"Error downloading data: {e}")

if dst_vars:
    # Extract the data
    dst_data = get_data(dst_vars[0])  # dst_vars[0] is usually 'kyoto_dst'
    
    if dst_data:
        times, values = dst_data
        
        # Convert to pandas DataFrame
        df = pd.DataFrame({
            'datetime': pd.to_datetime(times, unit='s'),
            'dst': values.flatten()
        })
        df.set_index('datetime', inplace=True)
        
        # Save to CSV
        df.to_csv('../data/pydata/geom_indices/kyoto/dst_data.csv')
        print(f"✓ Saved {len(df)} Dst records")
        print(f"Date range: {df.index.min()} to {df.index.max()}")
    else:
        print("✗ No data retrieved")
else:
    print("✗ Download failed")

#----------------------------------------------------------------------------
print("Everything done!")