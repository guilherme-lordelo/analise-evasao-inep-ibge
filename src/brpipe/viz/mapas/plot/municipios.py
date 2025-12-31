from brpipe.viz.mapas.config.inep import FORMULAS
from brpipe.viz.mapas.merge.municipios import merge_municipios
from brpipe.viz.mapas.config import PLOT, MUNICIPIOS
from brpipe.viz.mapas.plot.visualizacao import plot_mapa
from brpipe.viz.mapas.visoes.municipios import VisaoMunicipios

def mapa_evasao_municipios(
    formula_indice: int,
    sigla_uf: str | None = None,
    ano: int | None = None,
):
    
    try:
        formula_indice = int(formula_indice)
    except ValueError:
        raise ValueError(f'O indice "{formula_indice}" deve ser um número inteiro')
    gdf = merge_municipios()

    visao = VisaoMunicipios(gdf)
    visao.set_ano(ano)
    visao.set_uf(sigla_uf.upper() if sigla_uf else None)

    gdf_view = visao.get_view()

    gdf_view["geometry"] = gdf_view.geometry.simplify(
        tolerance=0.01,
        preserve_topology=True
    )

    plot_mapa(
        gdf=gdf_view,
        coluna=FORMULAS[formula_indice],
        figsize=MUNICIPIOS.figsize,
        cmap=PLOT.cmap,
        legend_label=MUNICIPIOS.legend_label,
        shrink=PLOT.legend_shrink,
        titulo=f"Evasão Municipal"
               f"{f' — {sigla_uf.upper()}' if sigla_uf else ''}"
               f"{f' ({ano})' if ano else ''}",
    )