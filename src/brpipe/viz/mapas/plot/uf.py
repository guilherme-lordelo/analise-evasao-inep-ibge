from brpipe.viz.mapas.merge.uf import merge_uf_evasao
from brpipe.viz.mapas.config.config import coluna_evasao, plot_cfg, uf_cfg
from brpipe.viz.mapas.plot.base import plot_mapa

def mapa_evasao_uf():
    coluna = coluna_evasao()
    gdf = merge_uf_evasao(coluna)

    plot_mapa(
        gdf=gdf,
        coluna=coluna,
        figsize=uf_cfg()["figsize"],
        cmap=plot_cfg()["cmap"],
        legend_label=uf_cfg()["legend_label"],
        shrink=plot_cfg()["legend_shrink"],
        titulo="Evasão Média por Estado",
    )
