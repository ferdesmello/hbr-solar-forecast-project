import os
import pandas as pd

#--------------------------------------------------------------------------- 
# Configuration
mode = "process"   # "download" or "process"

data_dir = "./goes_data"
year_dir = "./goes_data/goes_data_by_year"

start_date = '2010-01-01'
end_date = '2024-12-31'
probes = list(range(10, 17+1))  # GOES 10-17

#--------------------------------------------------------------------------- 
def process_existing():
    """Read existing per-probe files, split by year, and combine."""
    os.makedirs(year_dir, exist_ok=True)

    probe_files = [f for f in os.listdir(data_dir) if f.startswith("goes_") and f.endswith("_data.csv")]
    if not probe_files:
        print("✗ No per-probe CSVs found in goes_data")
        return

    all_dfs = []
    for file in probe_files:
        file_path = os.path.join(data_dir, file)
        print(f"Reading {file_path} ...")
        try:
            df = pd.read_csv(file_path, parse_dates=["datetime"], index_col="datetime")
        except Exception as e:
            print(f"  ✗ Could not read {file}: {e}")
            continue
        if df.empty:
            print(f"  ✗ {file} is empty")
            continue

        all_dfs.append(df)

        for year, df_year in df.groupby(df.index.year):
            year_file = os.path.join(year_dir, f"{file.replace('_data.csv','')}_{year}.csv")
            df_year.to_csv(year_file)
            print(f"  ✓ Wrote {len(df_year)} rows to {year_file}")

    if all_dfs:
        print("\nSaving combined GOES data...")
        combined = pd.concat(all_dfs, axis=1).sort_index()
        combined_file = os.path.join(data_dir, "goes_all_probes.csv")
        combined.to_csv(combined_file)
        print(f"✓ Combined {len(combined)} rows into {combined_file}")
        print(f"Date range: {combined.index.min()} to {combined.index.max()}")
    else:
        print("✗ No data combined")

#--------------------------------------------------------------------------- 
def download_data():
    """Download GOES data with pyspedas and save per-probe files."""
    import pyspedas
    from pytplot import get_data

    os.makedirs(data_dir, exist_ok=True)
    range_date = [start_date, end_date]

    print(f"Downloading GOES X-ray data for probes {probes[0]}-{probes[-1]}...")
    print(f"Date range: {range_date[0]} to {range_date[1]}")

    all_probe_data = []
    successful_probes = []

    for probe in probes:
        print(f"\nTrying GOES-{probe}...")
        try:
            goes_vars = pyspedas.projects.goes.xrs(
                trange=range_date, datatype='1min', probe=str(probe), time_clip=True
            )
            if not goes_vars:
                print(f"✗ GOES-{probe}: No data")
                continue

            frames = []
            for var in goes_vars:
                data = get_data(var)
                if data is None:
                    continue
                if len(data) == 2:
                    times, values = data
                elif len(data) == 3:
                    times, values, _ = data
                else:
                    continue

                df = pd.DataFrame({
                    "datetime": pd.to_datetime(times, unit="s"),
                    var: values.flatten() if values.ndim == 1 else values[:, 0]
                }).set_index("datetime")
                frames.append(df)
                print(f"  ✓ {var}: {len(df)} records")

            if frames:
                df_probe = pd.concat(frames, axis=1)
                out_file = f"{data_dir}/goes_{probe}_data.csv"
                df_probe.to_csv(out_file)
                print(f"  ✓ Saved {out_file} ({len(df_probe)} rows)")
                all_probe_data.append(df_probe)
                successful_probes.append(probe)

        except Exception as e:
            print(f"✗ GOES-{probe}: error {e}")

    if all_probe_data:
        print("\nSaving combined GOES data...")
        combined = pd.concat(all_probe_data, axis=1).sort_index()
        combined.to_csv(f"{data_dir}/goes_all_probes.csv")
        print(f"✓ Saved combined GOES data: {len(combined)} rows")
        print(f"Date range: {combined.index.min()} to {combined.index.max()}")
        print(f"Successful probes: {successful_probes}")

#--------------------------------------------------------------------------- 
if __name__ == "__main__":
    if mode == "process":
        process_existing()
    elif mode == "download":
        download_data()
    else:
        raise ValueError("mode must be 'download' or 'process'")