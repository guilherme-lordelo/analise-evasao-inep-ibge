import pandas as pd
from brpipe.viz.mapas.malhas.uf import carregar_malha_uf
from brpipe.viz.mapas.dados.uf import carregar_metrica_uf
from brpipe.viz.mapas.config import VARIAVEIS, MALHA

CHAVE_MALHA = MALHA.uf
CHAVE_TABELA = VARIAVEIS.territoriais["uf"]

def merge_uf() -> pd.DataFrame:
    gdf = carregar_malha_uf()
    df = carregar_metrica_uf()

    gdf[CHAVE_MALHA] = gdf[CHAVE_MALHA].astype(str)
    df[CHAVE_TABELA] = df[CHAVE_TABELA].astype(str)

    return gdf.merge(
        df,
        left_on=CHAVE_MALHA,
        right_on=CHAVE_TABELA,
        how="left"
    )
