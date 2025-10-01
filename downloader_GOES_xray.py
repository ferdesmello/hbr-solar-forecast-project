import os
import pyspedas
import pandas as pd
from pytplot import get_data

#---------------------------------------------------------------------------
# Configuration
start_date = '1995-01-01'
end_date = '2020-12-31'
range_date = [start_date, end_date]
probes = list(range(8, 18+1))  # GOES 8-18

#---------------------------------------------------------------------------
# Create output directory
os.makedirs("./goes_data", exist_ok=True)

print(f"Downloading GOES X-ray data for probes {probes[0]}-{probes[-1]}...")
print(f"Date range: {range_date[0]} to {range_date[1]}")

all_probe_data = []
successful_probes = []

#---------------------------------------------------------------------------
# Download GOES data
# Check https://pyspedas.readthedocs.io/en/latest/goes.html

print("Downloading GOES X-ray data...")

# Loop through all probes
for probe in probes:
    print(f"\nTrying GOES-{probe}...")
    
    try:
        goes_vars = pyspedas.projects.goes.xrs(
            trange=range_date, 
            datatype='1min', 
            probe=str(probe),
            time_clip=True
        )
        
        if goes_vars:
            print(f"✓ GOES-{probe}: Found variables {goes_vars}")
            
            frames = []
            
            for var in goes_vars:
                data = get_data(var)
                if data is None:
                    continue

                # data can be (times, values) or (times, values, extra)
                if len(data) == 2:
                    times, values = data
                elif len(data) == 3:
                    times, values, _ = data
                else:
                    continue

                # build DataFrame
                df = pd.DataFrame({
                    "datetime": pd.to_datetime(times, unit="s"),
                    var: values.flatten() if values.ndim == 1 else values[:, 0]
                })
                df.set_index("datetime", inplace=True)
                frames.append(df)
                print(f"  ✓ {var}: {len(df)} records")

            if frames:
                # join all variables on datetime for this probe
                df_probe = pd.concat(frames, axis=1)
                
                # Save individual probe file
                df_probe.to_csv(f"./goes_data/goes_{probe}_data.csv")
                print(f"  ✓ Saved GOES-{probe}: {len(df_probe)} records")
                
                # Add to combined list
                all_probe_data.append(df_probe)
                successful_probes.append(probe)
            else:
                print(f"  ✗ GOES-{probe}: No usable variables extracted")
        else:
            print(f"✗ GOES-{probe}: No data found")
            
    except Exception as e:
        print(f"✗ GOES-{probe}: Download error - {e}")
        continue

#---------------------------------------------------------------------------
# Combine all successful probes
if all_probe_data:
    print(f"\nCombining data from {len(successful_probes)} successful probes...")
    
    # Concatenate all probe data
    combined_data = pd.concat(all_probe_data, axis=1)
    combined_data = combined_data.sort_index()
    
    # Save combined file
    combined_data.to_csv("./goes_data/goes_all_probes.csv")
    print(f"✓ Saved combined GOES data: {len(combined_data)} records")
    print(f"Date range: {combined_data.index.min()} to {combined_data.index.max()}")
    print(f"Variables: {list(combined_data.columns)}")
    print(f"Successful probes: {successful_probes}")
    
    # Show data summary
    print(f"\nData overview:")
    print(f"  Total records: {len(combined_data):,}")
    print(f"  Total variables: {len(combined_data.columns)}")
    print(f"  File sizes:")
    for probe in successful_probes:
        file_path = f"./goes_data/goes_{probe}_data.csv"
        if os.path.exists(file_path):
            size_mb = os.path.getsize(file_path) / (1024*1024)
            print(f"    GOES-{probe}: {size_mb:.1f} MB")
    
else:
    print("✗ No GOES data downloaded from any probe")

print("\nDownload complete!")
print("Files saved in ./goes_data/ directory")

#---------------------------------------------------------------------------
print("Everything done!")