from brpipe.viz.mapas.malhas.municipios import carregar_malha_municipios
from brpipe.viz.mapas.dados.evasao import carregar_evasao_municipios
from brpipe.viz.mapas.config.config import colunas_municipio

malha = colunas_municipio()["malha"]
tabela = colunas_municipio()["tabela"]

def merge_municipios_evasao():
    gdf = carregar_malha_municipios()
    df = carregar_evasao_municipios()

    gdf[malha] = gdf[malha].astype(int)
    df[tabela] = df[tabela].astype(int)

    return gdf.merge(
        df,
        left_on=malha,
        right_on=tabela,
        how="left"
    )
