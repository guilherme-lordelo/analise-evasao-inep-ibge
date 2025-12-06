from functools import reduce
import pandas as pd
from pathlib import Path

from utils.io import read_csv
from utils.paths import PROCESSED_IBGE
from ibge.config import SHEETS_IBGE, COLUNAS_BASE_IBGE


def carregar_todos_ibge():
    """
    Retorna um DataFrame contendo todas as colunas finais do IBGE.
    """

    dfs = []

    for tabela_id, tabela_info in SHEETS_IBGE.items():

        for sheet in tabela_info["sheets"]:

            nome_csv = sheet["arquivo"]   # ex: tab12_rendimento_total.csv
            path = PROCESSED_IBGE / nome_csv

            if not path.exists():
                print(f"Aviso: arquivo IBGE não encontrado: {path}")
                continue

            df = read_csv(path)

            if COLUNAS_BASE_IBGE[0] not in df.columns:
                raise ValueError(
                    f"Arquivo {nome_csv} não contém a coluna '{COLUNAS_BASE_IBGE[0]}' (CO_MUNICIPIO)."
                )

            dfs.append(df)

    if not dfs:
        raise FileNotFoundError(
            f"Nenhum arquivo IBGE encontrado em {PROCESSED_IBGE}"
        )

    df_final = reduce(
        lambda left, right: pd.merge(
            left, right, on=COLUNAS_BASE_IBGE[0], how="outer"
        ),
        dfs
    )

    return df_final
