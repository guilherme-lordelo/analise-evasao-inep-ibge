import pandas as pd
from inep.config import VARIAVEIS_QUANTITATIVAS, get_campos_municipio

def agrega_por_municipio(df: pd.DataFrame) -> pd.DataFrame:
    # Quantitativas presentes no dataframe
    colunas_presentes = [c for c in df.columns if c in VARIAVEIS_QUANTITATIVAS]

    # Constrói lista de colunas de agrupamento
    colunas_groupby = get_campos_municipio(df)

    # Agrega
    return df.groupby(colunas_groupby, as_index=False)[colunas_presentes].sum()


def agrega_com_sufixo(df: pd.DataFrame, ano: str) -> pd.DataFrame:
    agg = agrega_por_municipio(df)

    # Renomeia APENAS quantitativas
    renomear = {
        col: f"{col}_{ano}"
        for col in agg.columns
        if col in VARIAVEIS_QUANTITATIVAS
    }

    return agg.rename(columns=renomear)
