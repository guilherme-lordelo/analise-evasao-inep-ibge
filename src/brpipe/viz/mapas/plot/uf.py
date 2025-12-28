from brpipe.viz.mapas.merge.uf import merge_uf_evasao
from brpipe.viz.mapas.config import DADOS, PLOT, UF
from brpipe.viz.mapas.plot.base import plot_mapa

def mapa_evasao_uf():
    gdf = merge_uf_evasao()

    plot_mapa(
        gdf=gdf,
        coluna=DADOS.metrica_principal.coluna_mapa,
        figsize=UF.figsize,
        cmap=PLOT.cmap,
        legend_label=UF.legend_label,
        shrink=PLOT.legend_shrink,
        titulo=f"Evasão Média por Estado",
    )
