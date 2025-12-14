# src/inep/load/loader_evasao.py

from utils.io import write_csv
from utils.paths import (
    arquivo_municipal,
    arquivo_estadual,
    arquivo_nacional,
)
from inep.carga.csv_saida import csv_kwargs_saida


ARQUIVOS = {
    "municipal": arquivo_municipal,
    "estadual": arquivo_estadual,
    "nacional": arquivo_nacional,
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

        df_saida, kwargs = csv_kwargs_saida(df)

        write_csv(df_saida, path, **kwargs)

        print(f"Arquivo salvo em '{path}'.")
