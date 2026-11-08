"""
Filters the raw monthly EIA total-energy pull down to just consumer
energy prices: gasoline, residential electricity, residential natural gas.
Run this after extract_total_energy_monthly.py has produced
eia_total_energy_monthly_raw.csv.
"""

import pandas as pd

SERIES_TO_KEEP = {
    "RMRTUUS": "Gasoline (Regular, All Areas)",   # $/gallon, incl. taxes
    "ESRCUUS": "Residential Electricity",          # cents/kWh, incl. taxes
    "NGRCUUS": "Residential Natural Gas",           # $/thousand cu ft
}

df = pd.read_csv("eia_total_energy_monthly_raw.csv")

filtered = df[df["msn"].isin(SERIES_TO_KEEP.keys())].copy()
filtered["fuel_type"] = filtered["msn"].map(SERIES_TO_KEEP)

# Split "period" (e.g. "2020-01") into separate year and month columns -
# useful for Power BI date hierarchies and SQL Server date handling.
filtered["year"] = filtered["period"].str[:4].astype(int)
filtered["month"] = filtered["period"].str[5:7].astype(int)

filtered = filtered.rename(columns={"value": "price"})
filtered = filtered[["period", "year", "month", "fuel_type", "price", "unit", "msn"]]
filtered = filtered.sort_values(["fuel_type", "period"]).reset_index(drop=True)

print(filtered.head(10))
print("...")
print(f"\nTotal rows: {len(filtered)}")

filtered.to_csv("consumer_energy_prices_monthly.csv", index=False)
print("Saved to consumer_energy_prices_monthly.csv")