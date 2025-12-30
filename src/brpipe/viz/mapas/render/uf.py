from brpipe.viz.mapas.merge.uf import merge_uf
from brpipe.viz.mapas.visoes.uf import VisaoUF
from brpipe.viz.mapas.render.getFiguras import render_mapa
from brpipe.viz.mapas.config import DADOS, PLOT, UF
from brpipe.utils.paths import MAPAS_RENDER
import matplotlib.pyplot as plt


def render_uf_por_ano():
    out_dir = MAPAS_RENDER / "uf"
    out_dir.mkdir(parents=True, exist_ok=True)

    anos = DADOS.metrica_principal.long.anos

    gdf = merge_uf()
    visao = VisaoUF(gdf)

    for ano in anos:
        visao.set_ano(ano)
        gdf_view = visao.get_view().copy()

        fig, ax = render_mapa(
            gdf=gdf_view,
            coluna=DADOS.metrica_principal.coluna_mapa,
            figsize=UF.figsize,
            cmap=PLOT.cmap,
            legend_label=UF.legend_label,
            shrink=PLOT.legend_shrink,
            titulo=f"Evasão por UF ({ano})",
        )

        out = out_dir / f"evasao_uf_{ano}.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
