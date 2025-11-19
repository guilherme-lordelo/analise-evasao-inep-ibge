import pandas as pd


def validar_linhas(df_merged: pd.DataFrame, ano_base: str, ano_seguinte: str) -> pd.DataFrame:
    col_M_n = f"QT_MAT_TOTAL_{ano_seguinte}"
    col_I_n = f"QT_ING_TOTAL_{ano_seguinte}"
    col_M_prev = f"QT_MAT_TOTAL_{ano_base}"
    col_C_prev = f"QT_CONC_TOTAL_{ano_base}"

    MIN_M_PREV = 10
    MIN_M_N = 5
    MIN_I_N = 1
    MIN_C_PREV = 1

    motivos = []

    for i in range(len(df_merged)):
        motivo = []

        M_prev = df_merged.at[i, col_M_prev]
        M_n = df_merged.at[i, col_M_n]
        I_n = df_merged.at[i, col_I_n]
        C_prev = df_merged.at[i, col_C_prev]

        if M_prev < MIN_M_PREV:
            motivo.append(f"M(n-1) < {MIN_M_PREV}")
        if M_n < MIN_M_N:
            motivo.append(f"M(n) < {MIN_M_N}")
        if I_n < MIN_I_N:
            motivo.append(f"I(n) < {MIN_I_N}")
        if C_prev < MIN_C_PREV:
            motivo.append(f"C(n-1) < {MIN_C_PREV}")

        if not (M_n - I_n > 0):
            motivo.append("M(n)-I(n) <= 0")
        if not (M_prev - C_prev > 0):
            motivo.append("M(n-1)-C(n-1) <= 0")
        if not ((M_n - I_n) <= (M_prev - C_prev)):
            motivo.append("M(n)-I(n) > M(n-1)-C(n-1)")

        if motivo:
            motivos.append("; ".join(motivo))
        else:
            motivos.append("válido")

    df_merged[f"EVASAO_VALIDACAO_{ano_base}_{ano_seguinte}"] = motivos
    df_merged[f"EVASAO_VALIDO_{ano_base}_{ano_seguinte}"] = (df_merged[f"EVASAO_VALIDACAO_{ano_base}_{ano_seguinte}"] == "válido")

    return df_merged
