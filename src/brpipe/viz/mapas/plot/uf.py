from brpipe.viz.mapas.merge.uf import merge_uf
from brpipe.viz.mapas.config import DADOS, PLOT, UF
from brpipe.viz.mapas.plot.base import plot_mapa
from brpipe.viz.mapas.visoes.uf import VisaoUF

def mapa_evasao_uf(ano: int | None = None):
    gdf = merge_uf()

    visao = VisaoUF(gdf)
    visao.set_ano(ano)

    gdf_view = visao.get_view()

    plot_mapa(
        gdf=gdf_view,
        coluna=DADOS.metrica_principal.coluna_mapa,
        figsize=UF.figsize,
        cmap=PLOT.cmap,
        legend_label=UF.legend_label,
        shrink=PLOT.legend_shrink,
        titulo=f"Evasão Média por Estado",
    )
