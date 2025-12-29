from brpipe.viz.mapas.malhas.uf import carregar_malha_uf
from brpipe.viz.mapas.dados.uf import carregar_metrica_uf
from brpipe.viz.mapas.config import COLUNAS

_uf = COLUNAS.territoriais.uf
MALHA = _uf.malha
TABELA = _uf.tabela

def merge_uf():
    gdf = carregar_malha_uf()
    df = carregar_metrica_uf()

    gdf[MALHA] = gdf[MALHA].astype(str)
    df[TABELA] = df[TABELA].astype(str)

    return gdf.merge(
        df,
        left_on=MALHA,
        right_on=TABELA,
        how="left"
    )
