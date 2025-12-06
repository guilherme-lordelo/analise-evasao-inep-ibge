# src/inep/uniao/uniao_municipios.py
import pandas as pd
from inep.config import get_campos_municipio

def unir_municipios(lista_dfs):
    """
    lista_dfs = lista de dataframes operacionais
    Une todos pelas colunas de identificação.
    """
    df_final = None
    campos_id = None

    for df in lista_dfs:
        if campos_id is None:
            campos_id = get_campos_municipio(df)

        if df_final is None:
            df_final = df
        else:
            df_final = pd.merge(
                df_final,
                df,
                on=campos_id,
                how="outer"
            )

    return df_final
