import pandas as pd
from inep.config import VARIAVEIS_YAML

def padronizar_categoricas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara variáveis categóricas para agregação LONG.

    - Converte categóricas em dummies.
    - Cada dummy segue o formato: VARIAVEL_VALOR.
    - Remove as colunas categóricas originais.
    """

    df_out = df.copy()

    for var in VARIAVEIS_YAML.categoricas:

        if var not in df_out.columns:
            continue

        valores_validos = VARIAVEIS_YAML.valores_categoricos.get(var, [])

        # Mapeia OUTROS
        serie = df_out[var].apply(
            lambda x: x if x in valores_validos else "OUTROS"
        )

        dummies = pd.get_dummies(
            serie,
            prefix=var,
            prefix_sep="_",
            dtype=float
        )

        colunas_previstas = [f"{var}_{v}" for v in valores_validos] + [f"{var}_OUTROS"]

        for col in colunas_previstas:
            if col not in dummies.columns:
                dummies[col] = 0.0

        dummies = dummies[colunas_previstas]  # ordenação padronizada

        df_out = pd.concat([df_out, dummies], axis=1)

        # Remove as colunas originais categóricas
        df_out.drop(columns=[var], inplace=True)
        
    return df_out
