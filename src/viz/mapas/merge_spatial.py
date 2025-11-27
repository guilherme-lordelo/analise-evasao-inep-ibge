import geopandas as gpd
import pandas as pd

from utils.paths import DATA_PROCESSED
from viz.mapas.carregar_malhas import carregar_malha_municipios


def carregar_evasao_final():
    """
    Carrega arquivo final pós-integração INEP + IBGE.
    """
    path = DATA_PROCESSED / "municipios_evasao_valida_ibge_2020_2024.csv"
    return pd.read_csv(path, sep=";")


def merge_malha_evasao():
    """
    Une a malha municipal IBGE com a tabela final de evasão.
    Retorna GeoDataFrame pronto para mapas temáticos.
    """
    gdf = carregar_malha_municipios()
    df = carregar_evasao_final()

    # Ajustar nomes de colunas
    cod_mun_malha = "CD_MUN" 
    cod_mun_tabela = "CO_MUNICIPIO"

    if cod_mun_malha not in gdf.columns:
        raise ValueError(f"Coluna {cod_mun_malha} não encontrada no shapefile.")

    # Garantir formato inteiro ou string consistente
    gdf[cod_mun_malha] = gdf[cod_mun_malha].astype(int)
    df[cod_mun_tabela] = df[cod_mun_tabela].astype(int)

    gdf_merged = gdf.merge(
        df,
        left_on=cod_mun_malha,
        right_on=cod_mun_tabela,
        how="left"
    )

    return gdf_merged
