import pandas as pd
from brpipe.viz.mapas.malhas.municipios import carregar_malha_municipios
from brpipe.viz.mapas.dados.municipios import carregar_metrica_municipios
from brpipe.viz.mapas.config import VARIAVEIS, MALHA

CHAVE_MALHA = MALHA.municipio
CHAVE_TABELA = VARIAVEIS.territoriais["municipio"]

def merge_municipios() -> pd.DataFrame:
    gdf = carregar_malha_municipios()
    df = carregar_metrica_municipios()

    gdf[CHAVE_MALHA] = gdf[CHAVE_MALHA].astype(int)
    df[CHAVE_TABELA] = df[CHAVE_TABELA].astype(int)

    return gdf.merge(
        df,
        left_on=CHAVE_MALHA,
        right_on=CHAVE_TABELA,
        how="left"
    )
