from brpipe.viz.mapas.merge.municipios import merge_municipios_evasao
from brpipe.viz.mapas.config.config import (
    coluna_evasao, plot_cfg, municipios_cfg
)
from brpipe.viz.mapas.plot.base import plot_mapa

def mapa_evasao_municipios(sigla_uf: str | None = None):
    gdf = merge_municipios_evasao()

    if sigla_uf:
        gdf = gdf[gdf["SIGLA_UF"] == sigla_uf.upper()]

    plot_mapa(
        gdf=gdf,
        coluna=coluna_evasao(),
        figsize=municipios_cfg()["figsize"],
        cmap=plot_cfg()["cmap"],
        legend_label=municipios_cfg()["legend_label"],
        shrink=plot_cfg()["legend_shrink"],
        titulo=f"Evasão Municipal {f'— {sigla_uf}' if sigla_uf else ''}",
    )
