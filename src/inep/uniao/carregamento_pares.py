from functools import reduce
import pandas as pd

from utils.io import read_csv
from utils.paths import PROCESSED_INEP

from inep.config import PARES, get_campos_municipio


def ler_pares_evasao():
    """Lê cada arquivo evasao_XXXX_YYYY.csv e retorna lista de DataFrames."""
    dfs = []
    campos_municipio = get_campos_municipio()

    for par in PARES:
        arquivo = PROCESSED_INEP / f"evasao_{par}.csv"

        df = read_csv(arquivo)

        # Seleciona TODAS as colunas do par dinâmico
        colunas_pares = [c for c in df.columns if c.endswith(f"_{par}")]

        # Mantém somente campos municipais + colunas do par
        df = df[campos_municipio + colunas_pares]

        dfs.append(df)

    return dfs

def merge_pares(dfs):
    """Merge sequencial por campos municipais configurados."""
    campos_municipio = get_campos_municipio()

    return reduce(
        lambda left, right: pd.merge(
            left, right,
            on=campos_municipio,
            how="outer"
        ),
        dfs
    )
