import pandas as pd

#----------------------------------------------------------------------------
# Read the data
df_omni = pd.read_csv("./omni_data/omni_data.csv")
df_dst = pd.read_csv("./pydata/geom_indices/kyoto/dst_data.csv")
#----------------------------------------------------------------------------
print("OMNI-----------------------------")
print(df_omni.shape)
print(df_omni.info())
print(df_omni.head())

print("Dst-----------------------------")
print(df_dst.shape)
print(df_dst.info())
print(df_dst.head())

#----------------------------------------------------------------------------

"""columns = [
    "datetime",
    "Rot#",
    "IMF",
    "PLS",
    "IMF_PTS",
    "PLS_PTS",
    "ABS_B",
    "F",
    "THETA_AV",
    "PHI_AV",
    "BX_GSE",
    "BY_GSE",
    "BZ_GSE",
    "BY_GSM",
    "BZ_GSM",
    "SIGMA-ABS_B",
    "SIGMA-B",
    "SIGMA-Bx",
    "SIGMA-By",
    "SIGMA-Bz",
    "T",
    "N",
    "V",
    "PHI-V",
    "THETA-V",
    "Ratio",
    "Pressure",
    "SIGMA-T",
    "SIGMA-N",
    "SIGMA-V",
    "SIGMA-PHI-V",
    "SIGMA-THETA-V",
    "SIGMA-ratio",
    "E",
    "Beta",
    "Mach_num",
    "Mgs_mach_num",
    "PR-FLX_1",
    "PR-FLX_2",
    "PR-FLX_4",
    "PR-FLX_10",
    "PR-FLX_30",
    "PR-FLX_60",
    "MFLX",
    "R",
    "F10_INDEX",
    "KP",
    "DST",
    "AE",
    "AP_INDEX",
    "AL_INDEX",
    "AU_INDEX",
    "PC_N_INDEX",
    "Solar_Lyman_alpha",
    "Proton_QI "
]"""

columns = [
    "datetime",
    "ABS_B",
    "BX_GSE",
    "BY_GSE",
    "BZ_GSE",
    "T",
    "Ratio",
    "Pressure",
]

df_short = df_omni[columns]

print("Short-----------------------------")
print(df_short.shape)
print(df_short.info())
print(df_short.head())

#----------------------------------------------------------------------------
# Save changes

df_short.to_csv('./Data/omni_data_filtered.csv', index=False)

#----------------------------------------------------------------------------

print("All done.")