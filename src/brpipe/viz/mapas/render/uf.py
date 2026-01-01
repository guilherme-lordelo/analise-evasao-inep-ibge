import pandas as pd
from brpipe.viz.mapas.config import PLOT, FORMULAS, ANOS
from brpipe.viz.mapas.merge.uf import merge_uf
from brpipe.viz.mapas.visoes.uf import VisaoUF
from brpipe.viz.mapas.render.getFiguras import render_mapa
from brpipe.utils.paths import MAPAS_RENDER
import matplotlib.pyplot as plt


def render_uf_por_ano() -> pd.DataFrame:
    out_dir = MAPAS_RENDER / "uf"

    gdf = merge_uf()
    visao = VisaoUF(gdf)

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
                titulo=f"{formula.replace("_", " ").title()} por UF ({ano})",
            )

            arquivo = out_formula / f"{formula.lower()}_uf_{ano}.png"
            fig.savefig(arquivo, dpi=150, bbox_inches="tight")
            plt.close(fig)
