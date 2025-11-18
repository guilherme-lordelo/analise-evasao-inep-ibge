import pandas as pd
from .carregamento_pares import PARES

def calcular_media_ponderada(df):
    evasao_cols = [f"TAXA_EVASAO_{p}" for p in PARES]
    peso_cols = [f"QT_ESTUDANTES_TOTAL_{p}" for p in PARES]

    df[evasao_cols + peso_cols] = df[evasao_cols + peso_cols].fillna(0)

    df["EVASAO_MEDIA_PONDERADA_2020_2024"] = (
        (df[evasao_cols].values * df[peso_cols].values).sum(axis=1)
        / df[peso_cols].sum(axis=1)
    )
    return df


def evasao_acumulada_ponderada(row, evasao_cols, peso_cols):
    prod = 1.0
    total_peso = row[peso_cols].sum()
    if total_peso == 0:
        return float('nan')

    for e_col, w_col in zip(evasao_cols, peso_cols):
        evasao = row[e_col]
        peso = row[w_col]
        if peso > 0 and not pd.isna(evasao):
            prod *= (1 - evasao) ** (peso / total_peso)

    return 1 - prod
