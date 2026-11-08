import requests
import pandas as pd
import time
import os
from dotenv import load_dotenv

load_dotenv("key.env")  # loads EIA_API_KEY from key.env (not committed)

BASE_URL = "https://api.eia.gov/v2/natural-gas/pri/sum/data/"
API_KEY = os.environ.get("EIA_API_KEY")

if not API_KEY:
    raise Exception("EIA_API_KEY not found. Make sure key.env exists and contains EIA_API_KEY=your_key_here")


def fetch_eia_data(start="2020-01", end="2026-05", length=5000):
    all_rows = []
    offset = 0

    while True:
        params = {
            "api_key": API_KEY,
            "frequency": "monthly",
            "data[0]": "value",
            "start": start,
            "end": end,
            "sort[0][column]": "period",
            "sort[0][direction]": "desc",
            "offset": offset,
            "length": length,
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

        payload = response.json()
        rows = payload.get("response", {}).get("data", [])

        if not rows:
            break

        all_rows.extend(rows)
        print(f"Pulled {len(rows)} rows (offset {offset}), total so far: {len(all_rows)}")

        if len(rows) < length:
            break

        offset += length
        time.sleep(0.5)

    return pd.DataFrame(all_rows)


if __name__ == "__main__":
    df = fetch_eia_data(start="2020-01", end="2026-05")

    print("\nShape:", df.shape)
    print("\nColumns:", df.columns.tolist())
    print("\nSample:")
    print(df.head())

    df.to_csv("eia_naturalgas_monthly_raw.csv", index=False)
    print("\nSaved to eia_naturalgas_monthly_raw.csv")