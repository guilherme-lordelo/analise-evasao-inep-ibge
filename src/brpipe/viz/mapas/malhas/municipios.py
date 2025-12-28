import geopandas as gpd
from brpipe.utils.paths import DATA_SHAPEFILES

def carregar_malha_municipios() -> gpd.GeoDataFrame:
    path = DATA_SHAPEFILES / "BR_Municipios_2024/BR_Municipios_2024.shp"
    gdf = gpd.read_file(path)

    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4674")

    return gdf
