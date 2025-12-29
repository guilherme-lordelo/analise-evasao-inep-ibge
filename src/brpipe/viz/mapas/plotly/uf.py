from brpipe.viz.mapas.merge.uf import merge_uf
from brpipe.viz.mapas.config import DADOS, COLUNAS
from brpipe.viz.mapas.visoes.uf import VisaoUF
from brpipe.viz.mapas.plotly.base import plot_mapa_plotly


def mapa_evasao_uf_plotly():
    gdf = merge_uf()

    visao = VisaoUF(gdf)

    gdf_view = visao.get_view()

    cols = COLUNAS.territoriais.uf

    fig = plot_mapa_plotly(
        gdf=gdf_view,
        coluna_valor=DADOS.metrica_principal.coluna_mapa,
        coluna_chave=cols.malha,          # ex: SIGLA_UF ou CD_UF
        coluna_ano=DADOS.metrica_principal.long.coluna_ano,
        titulo="Evasão Média por Estado (UF)",
    )

    fig.show()
