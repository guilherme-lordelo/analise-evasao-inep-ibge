import pandas as pd
from inep.config import VARIAVEIS_QUANTITATIVAS

def agrega_por_municipio(df: pd.DataFrame) -> pd.DataFrame:
    colunas_presentes = [c for c in df.columns if c in VARIAVEIS_QUANTITATIVAS]

    return df.groupby(
        ["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"],
        as_index=False
    )[colunas_presentes].sum()

def agrega_com_sufixo(df: pd.DataFrame, ano: str) -> pd.DataFrame:
    agg = agrega_por_municipio(df)

    renomear = {col: f"{col}_{ano}" for col in agg.columns if col in VARIAVEIS_QUANTITATIVAS}

    return agg.rename(columns=renomear)
