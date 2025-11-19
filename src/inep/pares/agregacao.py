import pandas as pd
from .carregamento_pares import PARES

def agrega_evasao(df, grupo):
    resultados = []

    for nivel, grupo_df in df.groupby(grupo):
        linha = {"NIVEL": nivel if grupo == "SG_UF" else "BRASIL"}

        for p in PARES:
            tx_col = f"TAXA_EVASAO_{p}"
            peso_col = f"QT_ESTUDANTES_TOTAL_{p}"
            total_peso = grupo_df[peso_col].sum()

            if total_peso == 0:
                linha[f"TAXA_EVASAO_{p}"] = float('nan')
            else:
                linha[f"TAXA_EVASAO_{p}"] = (
                    (grupo_df[tx_col] * grupo_df[peso_col]).sum() / total_peso
                )

            linha[peso_col] = total_peso

        resultados.append(linha)

    return pd.DataFrame(resultados)
