# src/inep/load/loader_evasao.py

from brpipe.utils.colunas_base import COL_NACIONAL
from brpipe.utils.io import write_csv
from brpipe.utils.paths import (
    inep_municipal,
    inep_estadual,
    inep_nacional,
)
from brpipe.inep.carga.csv_saida import csv_kwargs_saida


ARQUIVOS = {
    "municipal": inep_municipal,
    "estadual": inep_estadual,
    "nacional": inep_nacional,
}


def salvar_resultados(dfs_calculados: dict):
    """
    Escreve os DataFrames INEP finais.
    """

    if not isinstance(dfs_calculados, dict):
        raise TypeError("dfs_calculados deve ser um dicionário.")

    for nivel, df in dfs_calculados.items():
        if df is None:
            raise ValueError(f"Resultado para nível '{nivel}' não encontrado.")

        try:
            path = ARQUIVOS[nivel]
        except KeyError:
            raise ValueError(f"Nível desconhecido: '{nivel}'")
        print(df.columns)
        if nivel == "nacional":
            df.rename(columns={'UF_x': COL_NACIONAL}, inplace=True)
        print(df.columns)
        df_saida, kwargs = csv_kwargs_saida(df)

        write_csv(df_saida, path, **kwargs)

        print(f"Arquivo salvo em '{path}'.")
