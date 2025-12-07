import pandas as pd
from inep.config import (
    VARIAVEIS_CATEGORICAS,
    VARIAVEIS_QUANTITATIVAS,
    variaveis_cfg,
    get_campos_municipio,
    COLUNA_PESO,
)

# ================================================================
# Agregação de Variáveis Quantitativas
# ================================================================

def agrega_quantitativas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Soma as variáveis quantitativas por município.
    """
    colunas_presentes = [c for c in df.columns if c in VARIAVEIS_QUANTITATIVAS]
    colunas_groupby = get_campos_municipio(df)

    return df.groupby(colunas_groupby, as_index=False)[colunas_presentes].sum()


def agrega_quantitativas_com_sufixo(df: pd.DataFrame, ano: int | str) -> pd.DataFrame:
    """
    Agrega quantitativas e adiciona sufixo _{ano} somente às quantitativas.
    """
    agg = agrega_quantitativas(df)

    renomear = {
        col: f"{col}_{ano}"
        for col in agg.columns
        if col in VARIAVEIS_QUANTITATIVAS
    }

    return agg.rename(columns=renomear)


# ================================================================
# Agregação de Variáveis Categóricas
# ================================================================

def agrega_categoricas(df: pd.DataFrame, ano_base: int, ano_seguinte: int) -> pd.DataFrame:
    """
    Agrega variáveis categóricas calculando porcentagens ponderadas por município,
    usando a coluna definida em COLUNA_PESO.
    """

    # -----------------------------------
    # Criar coluna de peso interna
    # -----------------------------------
    expr_peso = COLUNA_PESO
    if expr_peso not in df.columns:
        raise ValueError(
            f"A coluna definida por COLUNA_PESO ('{expr_peso}') não existe no dataframe."
        )

    nome_peso = f"PESO_{ano_base}_{ano_seguinte}"

    df = df.copy()
    df[nome_peso] = df[expr_peso]

    campos_municipio = get_campos_municipio(df)

    # Remover quantitativas
    df_cat = df.drop(
        columns=[c for c in df.columns if c in VARIAVEIS_QUANTITATIVAS],
        errors="ignore"
    )

    # Manter apenas categóricas definidas
    cols_cat = [c for c in df_cat.columns if c in VARIAVEIS_CATEGORICAS]

    # Normalização
    for col in cols_cat:
        df_cat[col] = df_cat[col].astype("float", errors="ignore").astype("Int64", errors="ignore")

    resultados = []

    # ---------------------------------------------------------
    # Agregação por categoria
    # ---------------------------------------------------------
    for col in cols_cat:

        valores_yaml = list(variaveis_cfg["categoricas"][col]["valores"].keys())

        # CLASSIFICAÇÃO: YAML vs fora do YAML
        df_cat["_TMP_CAT"] = df_cat[col].apply(
            lambda x: x if x in valores_yaml else "_OUTROS"
        )

        # Agrupamento e soma ponderada
        df_val = (
            df_cat
            .groupby(campos_municipio + ["_TMP_CAT"])[nome_peso]
            .sum()
            .unstack(fill_value=0)
        )

        # Garantir colunas para todos os valores do YAML + OUTROS
        colunas_finais = valores_yaml + ["_OUTROS"]
        for val in colunas_finais:
            if val not in df_val.columns:
                df_val[val] = 0

        df_val = df_val[colunas_finais]

        # Cálculo de porcentagens
        soma_total = df_val.sum(axis=1).replace(0, pd.NA)
        df_pct = df_val.div(soma_total, axis=0) * 100

        # Renomear colunas
        df_pct.columns = [
            f"{col}_{val}_{ano_base}_{ano_seguinte}"
            for val in colunas_finais
        ]

        resultados.append(df_pct)

    # ---------------------------------------------------------
    # Combinação final
    # ---------------------------------------------------------
    if not resultados:
        return df_cat[campos_municipio].drop_duplicates()

    df_final = pd.concat(resultados, axis=1).reset_index()

    # ---------------------------------------------------------
    # Adiciona peso total por município
    # ---------------------------------------------------------
    pesos_agr = (
        df.groupby(campos_municipio)[nome_peso].sum().reset_index()
    )

    df_final = df_final.merge(pesos_agr, on=campos_municipio, how="left")

    return df_final
