import plotly.express as px
import geopandas as gpd
from brpipe.viz.mapas.config.inep import FORMULAS


def plot_mapa_plotly(
    gdf: gpd.GeoDataFrame,
    coluna_chave: str,
    coluna_ano: str,
    indice,
    titulo: str = "",
    color_continuous_scale: str = "Viridis",
):
    if gdf.empty:
        raise ValueError("GeoDataFrame vazio")

    geojson = gdf.dissolve(by=coluna_chave).geometry.__geo_interface__

    fig = px.choropleth(
        gdf,
        geojson=geojson,
        locations=coluna_chave,
        color=FORMULAS[indice],
        animation_frame=coluna_ano,
        color_continuous_scale=color_continuous_scale,
        title=titulo,
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
    )

    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0}
    )

    return fig
