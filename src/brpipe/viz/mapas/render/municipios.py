import pandas as pd
from brpipe.viz.mapas.config import PLOT, FORMULAS, ANOS
from brpipe.viz.mapas.merge.municipios import merge_municipios
from brpipe.viz.mapas.visoes.municipios import VisaoMunicipios
from brpipe.viz.mapas.render.getFiguras import render_mapa
from brpipe.utils.paths import MAPAS_RENDER
import matplotlib.pyplot as plt


def render_municipios_por_ano() -> pd.DataFrame:
    out_dir = MAPAS_RENDER / "municipios"

    gdf = merge_municipios()
    gdf["geometry"] = gdf.geometry.simplify(
    tolerance=0.01,
    preserve_topology=True,
    )
    visao = VisaoMunicipios(gdf)

    for formula in FORMULAS:
        out_formula = out_dir / f"{formula.lower()}"
        out_formula.mkdir(parents=True, exist_ok=True)

        for ano in ANOS:
            visao.set_ano(ano)
            gdf_view = visao.get_view().copy()

            fig, ax = render_mapa(
                gdf=gdf_view,
                coluna=formula,
                figsize=PLOT.figsize,
                cmap=PLOT.cmap,
                legend_label="Porcentagem",
                shrink=PLOT.legend_shrink,
                titulo=f"{formula.replace("_", " ").title()} por Município ({ano})",
            )

            arquivo = out_formula / f"{formula.lower()}_municipios_{ano}.png"
            fig.savefig(arquivo, dpi=150, bbox_inches="tight")
            plt.close(fig)
