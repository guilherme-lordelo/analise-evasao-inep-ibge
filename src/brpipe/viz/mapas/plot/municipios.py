from brpipe.viz.mapas.merge.municipios import merge_municipios
from brpipe.viz.mapas.config import DADOS, PLOT, MUNICIPIOS
from brpipe.viz.mapas.plot.base import plot_mapa
from brpipe.viz.mapas.visoes.municipios import VisaoMunicipios

def mapa_evasao_municipios(
    sigla_uf: str | None = None,
    ano: int | None = None,
):
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
        coluna=DADOS.metrica_principal.coluna_mapa,
        figsize=MUNICIPIOS.figsize,
        cmap=PLOT.cmap,
        legend_label=MUNICIPIOS.legend_label,
        shrink=PLOT.legend_shrink,
        titulo=f"Evasão Municipal"
               f"{f' — {sigla_uf.upper()}' if sigla_uf else ''}"
               f"{f' ({ano})' if ano else ''}",
    )