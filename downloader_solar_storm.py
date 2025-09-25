import pandas as pd
import requests
from io import StringIO

#---------------------------------------------------------------------------

# Example: download GOES-15 1-min averaged XRS flux for 2015
url = "https://satdat.ngdc.noaa.gov/sem/goes/data/full/2015/goes15/csv/g15_xrs_1m_20150101_20151231.csv"
r = requests.get(url)
df_flux = pd.read_csv(StringIO(r.text), comment='#')

#---------------------------------------------------------------------------
# Download flare list for 2015
flare_url = "https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_2015.txt"
flare_df = pd.read_fwf(flare_url, widths=[6,5,5,5,7,7,5,5,5], header=None)

#---------------------------------------------------------------------------
print(df_flux.head())
print(flare_df.head())

#---------------------------------------------------------------------------
print("Everything done!")