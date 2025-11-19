import pandas as pd
from .carregamento_pares import PARES

def separar_validos_invalidos(df):
    valid_cols = [f"EVASAO_VALIDO_{p}" for p in PARES]
    df["todos_validos"] = df[valid_cols].all(axis=1)

    return (
        df[df["todos_validos"]].copy(),
        df[~df["todos_validos"]].copy()
    )
