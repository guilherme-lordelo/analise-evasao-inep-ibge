from pathlib import Path
from functools import reduce
import pandas as pd

from utils.io import read_csv
from utils.paths import DATA_PROCESSED

PARES = ["2020_2021", "2021_2022", "2022_2023", "2023_2024"]

def ler_pares_evasao():
    """Lê cada arquivo evasao_XXXX_YYYY.csv e retorna lista de DataFrames."""
    dfs = []
    for p in PARES:
        arquivo = DATA_PROCESSED / f"evasao_{p}.csv"
        df = read_csv(arquivo, sep=";", encoding="utf-8", low_memory=False)
        df = df[
            ["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO",
             f"TAXA_EVASAO_{p}", f"EVASAO_VALIDO_{p}", f"QT_ESTUDANTES_TOTAL_{p}"]
        ]
        dfs.append(df)
    return dfs


def merge_pares(dfs):
    """Merge sequencial por CO_MUNICIPIO"""
    return reduce(
        lambda left, right: pd.merge(
            left, right,
            on=["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"],
            how="outer"
        ),
        dfs
    )
