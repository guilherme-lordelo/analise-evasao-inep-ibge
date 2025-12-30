from brpipe.viz.mapas.merge.municipios import merge_municipios
from brpipe.viz.mapas.visoes.municipios import VisaoMunicipios
from brpipe.viz.mapas.render.getFiguras import render_mapa
from brpipe.viz.mapas.config import DADOS, PLOT, MUNICIPIOS
from brpipe.utils.paths import MAPAS_RENDER
import matplotlib.pyplot as plt


def render_municipios_por_ano():
    out_dir = MAPAS_RENDER / "municipios"
    out_dir.mkdir(parents=True, exist_ok=True)

    anos = DADOS.metrica_principal.long.anos

    gdf = merge_municipios()
    visao = VisaoMunicipios(gdf)

    for ano in anos:
        visao.set_ano(ano)
        gdf_view = visao.get_view().copy()

        gdf_view["geometry"] = gdf_view.geometry.simplify(
            tolerance=0.01,
            preserve_topology=True,
        )

        fig, ax = render_mapa(
            gdf=gdf_view,
            coluna=DADOS.metrica_principal.coluna_mapa,
            figsize=MUNICIPIOS.figsize,
            cmap=PLOT.cmap,
            legend_label=MUNICIPIOS.legend_label,
            shrink=PLOT.legend_shrink,
            titulo=f"Evasão Municipal ({ano})",
        )

        out = out_dir / f"evasao_municipios_{ano}.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
