from brpipe.viz.mapas.merge.uf import merge_uf
from brpipe.viz.mapas.config import PLOT, UF
from brpipe.viz.mapas.plot.visualizacao import plot_mapa
from brpipe.viz.mapas.visoes.uf import VisaoUF
from brpipe.viz.mapas.config import FORMULAS

def mapa_evasao_uf(formula_indice: int, ano: int | None = None):
    gdf = merge_uf()

    visao = VisaoUF(gdf)
    visao.set_ano(ano)

    gdf_view = visao.get_view()

    plot_mapa(
        gdf=gdf_view,
        coluna=FORMULAS[formula_indice],
        figsize=UF.figsize,
        cmap=PLOT.cmap,
        legend_label=UF.legend_label,
        shrink=PLOT.legend_shrink,
        titulo=f"Evasão Média por Estado",
    )
