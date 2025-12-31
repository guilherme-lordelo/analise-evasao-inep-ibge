from brpipe.viz.mapas.config import VARIAVEIS, FORMULAS
from brpipe.viz.mapas.merge.uf import merge_uf
from brpipe.viz.mapas.config import COLUNAS
from brpipe.viz.mapas.visoes.uf import VisaoUF
from brpipe.viz.mapas.plotly.base import plot_mapa_plotly


def mapa_evasao_uf_plotly(formula_indice):

    try:
        formula_indice = int(formula_indice)
    except ValueError:
        raise ValueError(f'O indice "{formula_indice}" deve ser um número inteiro')
    gdf = merge_uf()

    visao = VisaoUF(gdf)

    gdf_view = visao.get_view()

    cols = COLUNAS.territoriais.uf

    fig = plot_mapa_plotly(
        gdf=gdf_view,
        coluna_chave=cols.malha,
        coluna_ano=VARIAVEIS.coluna_ano,
        titulo=f"{FORMULAS[formula_indice]} (UF)",
        indice=formula_indice,
    )

    fig.show()
