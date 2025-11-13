# fetch_sharp_keywords.py
import drms
import pandas as pd
from datetime import datetime, timedelta
import os
import time

#---------------------------------------------------------------------------
# Configuration
start_date = datetime(2010, 5, 1)   # SHARP starts ~2010-05
day = timedelta(days=1)
end_date   = datetime(2024, 12, 31) + day
current = start_date

out_dir = "../data/sharp_data/sharp_daily"
os.makedirs(out_dir, exist_ok=True)

# A JSOC valid email. Register here: http://jsoc.stanford.edu/ajax/register_email.html
c = drms.Client(email="fdesmello@gmail.com")

# Metadata query: get keywords, not segments
# Check http://jsoc.stanford.edu/doc/data/hmi/sharp/old/sharp.MB.htm
# And http://jsoc.stanford.edu/doc/keywords/JSOC_Keywords_for_metadata.pdf
keys = [
    'DATE-OBS', 
    'T_OBS', 
    'T_REC',
    'USFLUX', 
    'MEANGAM', 
    'MEANGBT', 
    'MEANGBZ', 
    'MEANGBH', 
    'MEANJZD', 
    'TOTUSJZ', 
    'MEANALP', 
    'MEANJZH', 
    'TOTUSJH', 
    'ABSNJZH', 
    'SAVNCPP', 
    'MEANPOT', 
    'TOTPOT', 
    'MEANSHR', 
    'SHRGT45', 
    'R_VALUE',
    'AREA_ACR',
    'HARPNUM',
]

#------------------------------------------------------------------
# Loop over days
while current < end_date:
    next_day = current + day
    fname = f"{out_dir}/{current.strftime('%Y%m%d')}.csv"
    if os.path.exists(fname):
        print("Skipping existing:", fname)
    else:
        qstr = f"hmi.sharp_720s[][{current.strftime('%Y.%m.%d_%H:%M:%S_TAI')}-{next_day.strftime('%Y.%m.%d_%H:%M:%S_TAI')}]"
        print("Querying:", qstr)

        retries = 0
        max_retries = 5
        while retries < max_retries:
            try:
                df = c.query(qstr, key=keys)
                if not df.empty:
                    df.to_csv(fname, index=False)
                    print("Saved", fname, "with", df.shape[0], "rows")
                else:
                    # Save empty file but with headers
                    pd.DataFrame(columns=keys).to_csv(fname, index=False)
                    print("No data for", fname, "(empty with headers)")
                break  # success → exit retry loop
            except Exception as e:
                retries += 1
                wait = 30 * retries
                print(f"Error: {e}. Retry {retries}/{max_retries} in {wait} s...")
                time.sleep(wait)
        else:
            print("Failed after max retries:", fname)
            # Do not advance, so you can rerun later
            break

    current = next_day

#------------------------------------------------------------------
# Glue all CSVs into one DataFrame
print("\nCombining daily files...")
all_dfs = []
for f in sorted(os.listdir(out_dir)):
    if f.endswith(".csv"):
        try:
            df = pd.read_csv(os.path.join(out_dir, f))
            if not df.empty:
                all_dfs.append(df)
        except pd.errors.EmptyDataError:
            print("Skipping malformed empty file:", f)

if all_dfs:
    big_df = pd.concat(all_dfs, ignore_index=True)
    big_df.to_csv("../data/sharp_data/sharp_data.csv", index=False)
    print("Final saved sharp_data.csv with", big_df.shape[0], "rows")
else:
    print("No data collected.")

#---------------------------------------------------------------------------
print("Everything done!")