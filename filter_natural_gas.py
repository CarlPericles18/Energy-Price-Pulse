"""
Filters the raw monthly EIA natural gas pull down to just the national
residential price series.
Run this after eia_naturalgas_monthly.py has produced
eia_naturalgas_monthly_raw.csv.
"""

import pandas as pd

TARGET_SERIES_DESCRIPTION = "U.S. Price of Natural Gas Delivered to Residential Consumers (Dollars per Thousand Cubic Feet)"

df = pd.read_csv("eia_naturalgas_monthly_raw.csv")

filtered = df[df["series-description"] == TARGET_SERIES_DESCRIPTION].copy()

filtered = filtered.rename(columns={"value": "price", "units": "unit"})
filtered["fuel_type"] = "Residential Natural Gas"
filtered = filtered[["period", "fuel_type", "price", "unit", "series"]]
filtered = filtered.sort_values("period").reset_index(drop=True)

print(filtered.head())
print("...")
print(f"\nTotal rows: {len(filtered)}")

filtered.to_csv("naturalgas_monthly_filtered.csv", index=False)
print("Saved to naturalgas_monthly_filtered.csv")