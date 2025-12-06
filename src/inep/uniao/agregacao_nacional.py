# src/inep/uniao/agregacao_nacional.py
import pandas as pd
from inep.config import get_campos_municipio

def agregar_nacional(df_estadual):
    """
    Agrega os Estados em uma linha singular "BRASIL".
    """
    campo_uf = get_campos_municipio(df_estadual)[1]

    col_num = [
        c for c in df_estadual.columns
        if c != campo_uf and df_estadual[c].dtype != "object"
    ]

    df_brasil = pd.DataFrame({
        campo_uf: ["BRASIL"],
        **{c: [df_estadual[c].sum()] for c in col_num}
    })

    return df_brasil
