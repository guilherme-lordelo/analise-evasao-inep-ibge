# src/inep/uniao/agregacao_estadual.py
from inep.config import get_campos_municipio

def agregar_estadual(df_municipios):
    """
    Agrega todos os indicadores por UF.
    """

    campos_id = get_campos_municipio(df_municipios)
    campo_uf = campos_id[1]

    col_num = [
        c for c in df_municipios.columns
        if c not in campos_id and df_municipios[c].dtype != "object"
    ]

    df_estado = (
        df_municipios.groupby(campo_uf, as_index=False)[col_num].sum()
    )

    return df_estado
