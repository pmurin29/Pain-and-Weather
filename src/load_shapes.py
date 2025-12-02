import pandas as pd
import cartopy.io.shapereader as shpreader

def load_country_centroids(shapefile_path: str) -> pd.DataFrame:
    """
    Load a country shapefile and return a DataFrame of centroids.

    Parameters
    ----------
    shapefile_path : str
        Path to a Natural Earth admin-0 countries shapefile.

    Returns
    -------
    pandas.DataFrame
        Columns: ['iso_a3', 'centroid_lon', 'centroid_lat']
    """
    reader = shpreader.Reader(shapefile_path)
    records = list(reader.records())

    rows = []
    for rec in records:
        iso = rec.attributes.get("ISO_A3")
        geom = rec.geometry
        centroid = geom.centroid
        rows.append(
            {
                "iso_a3": iso,
                "centroid_lon": centroid.x,
                "centroid_lat": centroid.y,
            }
        )

    return pd.DataFrame(rows)
