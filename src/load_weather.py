import xarray as xr
import pandas as pd
from typing import Tuple

def _select_surface(field: xr.DataArray) -> xr.DataArray:
    """Pick level=1000 if a 'level' dimension exists, else return as-is."""
    if "level" in field.dims:
        return field.sel(level=1000)
    return field

def _extract_series(
    field: xr.DataArray,
    lon: float,
    lat: float,
    colname: str,
    scale: float = 1.0,
) -> pd.DataFrame:
    """Extract a nearest-gridpoint time series for a single location."""
    ts = field.sel(lon=lon, lat=lat, method="nearest")
    df = ts.to_dataframe().reset_index()
    df[colname] = df[ts.name] * scale
    return df[["time", colname]]

def load_weather_timeseries(
    nc_air: str,
    nc_slp: str,
    nc_shum: str,
    country_centroids: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load NCEP/NCAR weather data and extract country-level time series.

    Parameters
    ----------
    nc_air, nc_slp, nc_shum : str
        Paths to NetCDF files containing air temperature (K or °C),
        sea-level pressure (Pa), and specific humidity (kg/kg).
    country_centroids : DataFrame
        Output from ``load_country_centroids``.

    Returns
    -------
    (air_df, slp_df, shum_df) : tuple of DataFrames
        Each has columns ['time', var, 'iso_a3'] where
        var is 'air_C', 'slp_hPa', or 'shum_kgkg'.
    """
    air_ds = xr.open_dataset(nc_air)
    slp_ds = xr.open_dataset(nc_slp)
    shum_ds = xr.open_dataset(nc_shum)

    air_field = _select_surface(air_ds["air"])
    slp_field = slp_ds["slp"]
    shum_field = _select_surface(shum_ds["shum"])

    air_list, slp_list, shum_list = [], [], []

    for _, row in country_centroids.iterrows():
        lon = row["centroid_lon"]
        lat = row["centroid_lat"]
        iso = row["iso_a3"]

        # temperature (assumed °C or K already converted beforehand)
        df_air = _extract_series(air_field, lon, lat, "air_C", scale=1.0)
        df_air["iso_a3"] = iso
        air_list.append(df_air)

        # sea-level pressure: Pa -> hPa
        df_slp = _extract_series(slp_field, lon, lat, "slp_hPa", scale=1 / 100.0)
        df_slp["iso_a3"] = iso
        slp_list.append(df_slp)

        # specific humidity (kg/kg)
        df_shum = _extract_series(shum_field, lon, lat, "shum_kgkg", scale=1.0)
        df_shum["iso_a3"] = iso
        shum_list.append(df_shum)

    air_df = pd.concat(air_list, ignore_index=True)
    slp_df = pd.concat(slp_list, ignore_index=True)
    shum_df = pd.concat(shum_list, ignore_index=True)

    return air_df, slp_df, shum_df
