"""
Filters the raw weekly EIA gasoline pull down to just the national
Regular grade retail price series.
Run this after extract_gasoline_weekly.py has produced
eia_gasoline_weekly_raw.csv.
"""

import pandas as pd

TARGET_SERIES_DESCRIPTION = "U.S. Regular All Formulations Retail Gasoline Prices (Dollars per Gallon)"

df = pd.read_csv("eia_gasoline_weekly_raw.csv")

filtered = df[df["series-description"] == TARGET_SERIES_DESCRIPTION].copy()

filtered = filtered.rename(columns={"value": "price", "units": "unit"})
filtered["fuel_type"] = "Gasoline (Regular, All Areas)"
filtered = filtered[["period", "fuel_type", "price", "unit", "series"]]
filtered = filtered.sort_values("period").reset_index(drop=True)

print(filtered.head())
print("...")
print(f"\nTotal rows: {len(filtered)}")

filtered.to_csv("gasoline_weekly_filtered.csv", index=False)
print("Saved to gasoline_weekly_filtered.csv")