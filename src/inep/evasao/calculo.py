import pandas as pd
import numpy as np


def calcular_taxa_evasao(df: pd.DataFrame, ano_base: str, ano_seguinte: str) -> pd.DataFrame:
    col_M_n = f"QT_MAT_TOTAL_{ano_seguinte}"
    col_I_n = f"QT_ING_TOTAL_{ano_seguinte}"
    col_M_prev = f"QT_MAT_TOTAL_{ano_base}"
    col_C_prev = f"QT_CONC_TOTAL_{ano_base}"

    validos = df[f"EVASAO_VALIDO_{ano_base}_{ano_seguinte}"]
    evasao = pd.Series(np.nan, index=df.index, dtype="float64")

    M_n = df[col_M_n]
    I_n = df[col_I_n]
    M_prev = df[col_M_prev]
    C_prev = df[col_C_prev]

    evasao.loc[validos] = 1.0 - ((M_n.loc[validos] - I_n.loc[validos]) /
                                 (M_prev.loc[validos] - C_prev.loc[validos]))

    df[f"TAXA_EVASAO_{ano_base}_{ano_seguinte}"] = evasao.round(4)

    df[f"QT_ESTUDANTES_TOTAL_{ano_base}_{ano_seguinte}"] = (
        df[col_M_prev] + df[col_I_n]
    )

    return df
