from functools import reduce
import pandas as pd
from pathlib import Path

from brpipe.utils.io import read_csv
from brpipe.utils.paths import PROCESSED_IBGE
from brpipe.ibge.config import COLUNAS_BASE_IBGE, TABELAS_IBGE


def carregar():
    """
    Retorna um DataFrame contendo todas as colunas finais do IBGE.
    """

    dfs = []

    for tabela in TABELAS_IBGE.values():

        for sheet in tabela.sheets:

            nome_csv = sheet.arquivo
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
