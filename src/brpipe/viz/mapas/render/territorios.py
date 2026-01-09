import pandas as pd
import matplotlib.pyplot as plt
from typing import Callable, Type
from brpipe.utils.parser import parse_bool
from brpipe.viz.mapas.config import PLOT, METRICAS, ANOS, VARIAVEIS
from brpipe.viz.mapas.merge.municipios import merge_municipios
from brpipe.viz.mapas.merge.uf import merge_uf
from brpipe.viz.mapas.render.getFiguras import render_mapa
from brpipe.utils.paths import MAPAS_RENDER
from brpipe.viz.mapas.visoes.municipios import VisaoMunicipios
from brpipe.viz.mapas.visoes.uf import VisaoUF


def _render_por_ano(
    *,
    nome: str,
    merge_fn: Callable[[], pd.DataFrame],
    visao_classe: Type,
    sufixo_arquivo: str,
    titulo_base: str,
) -> None:
    """
    Render genérico de mapas territoriais por ano.

    Parâmetros:
    - nome: pasta de saída (ex: 'municipios', 'uf')
    - merge_fn: função que retorna o GeoDataFrame base
    - visao_classe: classe da visão (VisaoMunicipios, VisaoUF, etc.)
    - sufixo_arquivo: usado no nome do arquivo ('municipios', 'uf')
    - titulo_base: texto base do título ('Município', 'UF')
    """

    out_dir = MAPAS_RENDER / nome
    out_dir.mkdir(parents=True, exist_ok=True)
    gdf_base = merge_fn()

    gdf_base["sem_inep"] = gdf_base[VARIAVEIS.coluna_ano].isna()

    gdf_base["geometry"] = gdf_base.geometry.simplify(
        tolerance=0.01,
        preserve_topology=True,
    )



    visao = visao_classe(gdf_base)

    for formula in METRICAS:
        print("    " + formula + "...")
        out_formula = out_dir / formula.lower()
        out_formula.mkdir(parents=True, exist_ok=True)

        for ano in ANOS:
            visao.set_ano(ano)
            gdf_view = visao.get_view().copy()

            gdf_view["sem_dado_ano"] = (
                ~gdf_view["sem_inep"] &
                ~gdf_view["_visivel_ano"]
            )

            gdf_view["sem_metrica"] = (
                ~gdf_view["sem_inep"] &
                ~gdf_view["sem_dado_ano"] &
                gdf_view[formula].isna()
            )

            mask_valido = (
                gdf_view["_visivel_ano"] &
                ~gdf_view["sem_inep"] &
                ~gdf_view["sem_metrica"]
            )
            
            gdf_view["com_metrica"] = mask_valido

            titulo = None
            if parse_bool(PLOT.mostrar_titulo):
                titulo = (
                    f"{formula.replace('_', ' ').title()} "
                    f"por {titulo_base} ({ano})"
                )

            fig, ax = render_mapa(
                gdf=gdf_view,
                coluna=formula,
                figsize=PLOT.figsize,
                cmap=PLOT.cmap,
                legend_label="Índice",
                shrink=PLOT.legend_shrink,
                titulo=titulo,
            )

            arquivo = out_formula / f"{formula.lower()}_{sufixo_arquivo}_{ano}.png"
            fig.savefig(arquivo, dpi=150, bbox_inches="tight")
            plt.close(fig)

def render_municipios() -> None:
    _render_por_ano(
        nome="municipios",
        merge_fn=merge_municipios,
        visao_classe=VisaoMunicipios,
        sufixo_arquivo="municipios",
        titulo_base="Município",
    )

def render_uf() -> None:
    _render_por_ano(
        nome="uf",
        merge_fn=merge_uf,
        visao_classe=VisaoUF,
        sufixo_arquivo="uf",
        titulo_base="UF",
    )
