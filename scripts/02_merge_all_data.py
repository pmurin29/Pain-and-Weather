"""
Step 2: Merge seasonal weather means with the epidemiologic dataset.
"""
import os
import pandas as pd
from src.merge_data import merge_weather_with_health

DATA_RAW = "data/raw"
DATA_PROCESSED = "data/processed"

HEALTH_CSV = os.path.join(DATA_RAW, "complete_dataset_HAQ_GDP.csv")


def main():
    os.makedirs(DATA_PROCESSED, exist_ok=True)

    df_health = pd.read_csv(HEALTH_CSV)

    air = pd.read_csv(os.path.join(DATA_PROCESSED, "seasonal_air.csv"))
    slp = pd.read_csv(os.path.join(DATA_PROCESSED, "seasonal_slp.csv"))
    shum = pd.read_csv(os.path.join(DATA_PROCESSED, "seasonal_shum.csv"))

    df_merged = merge_weather_with_health(df_health, air, slp, shum)

    out_path = os.path.join(DATA_PROCESSED, "complete_dataset_with_weather.csv")
    df_merged.to_csv(out_path, index=False)
    print(f"Wrote merged dataset to {out_path}")


if __name__ == "__main__":
    main()
