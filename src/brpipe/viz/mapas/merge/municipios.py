from brpipe.viz.mapas.malhas.municipios import carregar_malha_municipios
from brpipe.viz.mapas.dados.municipios import carregar_metrica_municipios
from brpipe.viz.mapas.config import COLUNAS

_municipio = COLUNAS.territoriais.municipio
MALHA = _municipio.malha
TABELA = _municipio.tabela

def merge_municipios_evasao():
    gdf = carregar_malha_municipios()
    df = carregar_metrica_municipios()

    gdf[MALHA] = gdf[MALHA].astype(int)
    df[TABELA] = df[TABELA].astype(int)

    return gdf.merge(
        df,
        left_on=MALHA,
        right_on=TABELA,
        how="left"
    )