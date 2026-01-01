from brpipe.viz.mapas.merge.uf import merge_uf
from brpipe.viz.mapas.config import PLOT, FORMULAS
from brpipe.viz.mapas.plot.visualizacao import plot_mapa
from brpipe.viz.mapas.visoes.uf import VisaoUF

def mapa_evasao_uf(formula_indice: int, ano: int | None = None):
    gdf = merge_uf()

    visao = VisaoUF(gdf)
    visao.set_ano(ano)

    gdf_view = visao.get_view()

    plot_mapa(
        gdf=gdf_view,
        coluna=FORMULAS[formula_indice],
        figsize=PLOT.figsize,
        cmap=PLOT.cmap,
        legend_label="Porcentagem",
        shrink=PLOT.legend_shrink,
        titulo=f"{FORMULAS[formula_indice]} {ano} por UF"
    )
