import pandas as pd
from .utils import month_to_season

def add_year_season(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Add year and season columns and compute seasonal means."""
    df = df.copy()
    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["season"] = df["month"].apply(month_to_season)
    out = (
        df.groupby(["iso_a3", "year", "season"])[value_col]
        .mean()
        .reset_index()
    )
    return out

def merge_weather_with_health(
    df_health: pd.DataFrame,
    seasonal_air: pd.DataFrame,
    seasonal_slp: pd.DataFrame,
    seasonal_shum: pd.DataFrame,
) -> pd.DataFrame:
    """Merge seasonal weather means onto the health dataset."""
    df = df_health.copy()
    df = df.merge(seasonal_air, on=["iso_a3", "year", "season"], how="left")
    df = df.merge(seasonal_slp, on=["iso_a3", "year", "season"], how="left")
    df = df.merge(seasonal_shum, on=["iso_a3", "year", "season"], how="left")
    return df
