from brpipe.viz.mapas.merge.municipios import merge_municipios_evasao
from brpipe.viz.mapas.config import DADOS, PLOT, MUNICIPIOS
from brpipe.viz.mapas.plot.base import plot_mapa

def mapa_evasao_municipios(sigla_uf: str | None = None):
    gdf = merge_municipios_evasao()

    if sigla_uf:
        gdf = gdf[gdf["SIGLA_UF"] == sigla_uf.upper()]

    plot_mapa(
        gdf=gdf,
        coluna=DADOS.metrica_principal.coluna_mapa,
        figsize=MUNICIPIOS.figsize,
        cmap=PLOT.cmap,
        legend_label=MUNICIPIOS.legend_label,
        shrink=PLOT.legend_shrink,
        titulo=f"Evasão Municipal {f'— {sigla_uf}' if sigla_uf else ''}",
    )
