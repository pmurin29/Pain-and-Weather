"""
Step 1: Extract country centroids and compute seasonal weather means.
"""
import os
import pandas as pd

from src.load_shapes import load_country_centroids
from src.load_weather import load_weather_timeseries
from src.merge_data import add_year_season

DATA_RAW = "data/raw"
DATA_PROCESSED = "data/processed"

SHAPEFILE = os.path.join(DATA_RAW, "ne_110m_admin_0_countries.shp")
AIR_NC = os.path.join(DATA_RAW, "air.mon.mean.nc")
SLP_NC = os.path.join(DATA_RAW, "slp.mon.mean.nc")
SHUM_NC = os.path.join(DATA_RAW, "shum.mon.mean.nc")


def main():
    os.makedirs(DATA_PROCESSED, exist_ok=True)

    # A. Country centroids
    centroids = load_country_centroids(SHAPEFILE)

    # B. Weather time series at centroids
    air_df, slp_df, shum_df = load_weather_timeseries(AIR_NC, SLP_NC, SHUM_NC, centroids)

    # C. Seasonal means
    air_seasonal = add_year_season(air_df, "air_C")
    slp_seasonal = add_year_season(slp_df, "slp_hPa")
    shum_seasonal = add_year_season(shum_df, "shum_kgkg")

    air_seasonal.to_csv(os.path.join(DATA_PROCESSED, "seasonal_air.csv"), index=False)
    slp_seasonal.to_csv(os.path.join(DATA_PROCESSED, "seasonal_slp.csv"), index=False)
    shum_seasonal.to_csv(os.path.join(DATA_PROCESSED, "seasonal_shum.csv"), index=False)


if __name__ == "__main__":
    main()
