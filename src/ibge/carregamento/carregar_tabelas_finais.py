from functools import reduce
import pandas as pd
from pathlib import Path

from utils.io import read_csv
from utils.paths import DATA_PROCESSED
from ibge.config.colunas import COLUNAS_POR_TABELA


def ler_tabelas_ibge():
    IBGE_DIR = DATA_PROCESSED / "ibge_csv_final"
    dfs = []

    for fname, cols in COLUNAS_POR_TABELA.items():
        path = IBGE_DIR / fname.replace(".csv", "_final.csv")

        if not path.exists():
            print(f"Aviso: arquivo IBGE não encontrado: {path}")
            continue

        df = read_csv(path, sep=";", encoding="utf-8", usecols=cols, low_memory=False)

        redundantes = ["SG_UF", "NO_MUNICIPIO_OU_CLASSE"]
        df = df.drop(columns=[c for c in redundantes if c in df.columns], errors="ignore")

        dfs.append(df)

    if not dfs:
        raise FileNotFoundError(
            "Nenhum arquivo IBGE encontrado em data/processed/ibge_csv_final/"
        )

    return reduce(lambda l, r: pd.merge(l, r, on="CO_MUNICIPIO", how="outer"), dfs)
