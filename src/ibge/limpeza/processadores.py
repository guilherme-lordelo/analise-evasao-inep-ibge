import numpy as np
import pandas as pd

def renomear_colunas(df, novos_nomes):
    """Renomeia colunas conforme lista fornecida."""
    if not novos_nomes:
        raise ValueError("Lista de novos nomes de colunas vazia.")
    if len(df.columns) != len(novos_nomes):
        print(
            f"Aviso: número de colunas ({len(df.columns)}) "
            f"diferente da lista fornecida ({len(novos_nomes)})."
        )
    df.columns = novos_nomes[:len(df.columns)]
    return df


def limpar_linhas(df):
    """
    Remove:
    - Linhas com duas primeiras colunas vazias
    - Linhas textuais nas últimas 10 linhas
    - Colunas vazias nas últimas 2 linhas
    - Linha final vazia
    - Substitui '-' por NaN
    """
    # Remove linhas tipo ';;'
    cond_invalidas = (
        (df.iloc[:, 0].isna() | (df.iloc[:, 0].astype(str).str.strip() == "")) &
        (df.iloc[:, 1].isna() | (df.iloc[:, 1].astype(str).str.strip() == ""))
    )
    df = df[~cond_invalidas].copy()

    # Substitui '-' por NaN
    df = df.replace("-", np.nan)

    # Detecta e remove linhas textuais nas últimas 10
    ultimas_linhas = df.tail(10)
    mask_texto = ultimas_linhas.apply(
        lambda linha: (
            sum(~linha.astype(str)
                    .str.replace(r"[\d\.,\-]", "", regex=True)
                    .str.strip().eq(""))
            / len(linha)
        ) > 0.7,
        axis=1,
    )
    if mask_texto.any():
        df = df.drop(ultimas_linhas[mask_texto].index)

    # Remove colunas vazias nas últimas duas linhas
    ultimas_2 = df.tail(2)
    colunas_sem_info = ultimas_2.columns[
        ultimas_2.isna().all() |
        (ultimas_2.astype(str).apply(lambda s: s.str.strip() == "").all())
    ]
    df = df.drop(columns=colunas_sem_info)

    # Remove última linha se completamente vazia
    if df.tail(1).isna().all(axis=1).iloc[0]:
        df = df.iloc[:-1]

    return df.reset_index(drop=True)
