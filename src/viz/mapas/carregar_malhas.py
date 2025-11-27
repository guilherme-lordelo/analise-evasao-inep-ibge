import geopandas as gpd
from utils.paths import DATA_SHAPEFILES

def carregar_malha_municipios():
    """
    Carrega a malha municipal do IBGE (2024).
    """
    pasta = DATA_SHAPEFILES / "BR_Municipios_2024"
    shapefile_path = pasta / "BR_Municipios_2024.shp"

    if not shapefile_path.exists():
        raise FileNotFoundError(f"Shapefile não encontrado em: {shapefile_path}")

    gdf = gpd.read_file(shapefile_path)

    if gdf.crs is None:
        print("Aviso: CRS não encontrado. Definindo EPSG:4674 (IBGE).")
        gdf = gdf.set_crs("EPSG:4674")
    else:
        print(f"CRS detectado: {gdf.crs}")

    return gdf

def carregar_malha_uf():
    pasta = DATA_SHAPEFILES / "BR_UF_2024"
    shapefile_path = pasta / "BR_UF_2024.shp"

    if not shapefile_path.exists():
        raise FileNotFoundError(f"Shapefile não encontrado em: {shapefile_path}")

    gdf = gpd.read_file(shapefile_path)

    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4674")

    return gdf
