import pyspedas
import pandas as pd
from pytplot import get_data

#---------------------------------------------------------------------------
# Configuration
start_date = '1995-01-01'
end_date = '2024-12-31'
range_date = [start_date, end_date]

print(f"Processing OMNI data from {start_date} to {end_date}...")

#---------------------------------------------------------------------------
# Download OMNI data
# Check https://pyspedas.readthedocs.io/en/latest/omni.html

print("Downloading OMNI data...")

try:
    omni_vars = pyspedas.projects.omni.data(trange=range_date, datatype='hourly')
except Exception as e:
    print(f"Error downloading data: {e}")
    omni_vars = []

if omni_vars:
    frames = []

    for var in omni_vars:
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

    if frames:
        # join all variables on datetime
        df_all = pd.concat(frames, axis=1)

        # Save to CSV
        df_all.to_csv("../data/omni_data/omni_data.csv")
        print(f"✓ Saved {len(df_all)} OMNI records")
        print(f"Date range: {df_all.index.min()} to {df_all.index.max()}")
    else:
        print("✗ No usable OMNI variables extracted")
else:
    print("✗ Download failed")

#---------------------------------------------------------------------------
print("Everything done!")
