import gc
import pandas as pd
from brpipe.inep.config import VARIAVEIS_YAML


def agrega_quantitativas(df: pd.DataFrame, nivel: str = "municipal") -> pd.DataFrame:
    """
    Agrega quantitativas no formato LONG

    nivel:
        - "municipal" : groupby por código e nome do município + ano
        - "estadual"  : groupby por UF + ano
        - "nacional"  : soma total por ano (UF="BRASIL")
    """

    colunas_quant = [c for c in VARIAVEIS_YAML.quantitativas if c in df.columns]

    ano = VARIAVEIS_YAML.coluna_ano

    if nivel == "municipal":
        colunas_groupby = VARIAVEIS_YAML.campos_padrao + [ano]

    elif nivel == "estadual":
        # segundo campo de get_campos_municipio é UF
        colunas_groupby = [VARIAVEIS_YAML.campos_padrao[1], ano]

    elif nivel == "nacional":
        colunas_groupby = [ano]

    else:
        raise ValueError("nivel deve ser 'municipal', 'estadual' ou 'nacional'")

    if nivel in ["municipal", "estadual"]:
        agg = (
            df.groupby(colunas_groupby, as_index=False)[colunas_quant]
              .sum()
        )

    else:  # nacional
        soma = (
            df.groupby([ano], as_index=False)[colunas_quant]
              .sum()
              .reset_index()
        )
        soma.insert(0, "UF", "BRASIL")
        agg = soma

    return agg

def descobrir_categoricas_presentes(df):
    """
    Retorna:
    {
        "TP_REDE": [
            ("TP_REDE_1", "TP_REDE_Publica"),
            ("TP_REDE_2", "TP_REDE_Privada"),
        ],
        "IN_CAPITAL": [
            ("IN_CAPITAL_0", "IN_CAPITAL_Capital"),
            ("IN_CAPITAL_1", "IN_CAPITAL_Nao_Capital"),
        ]
    }
    """
    presentes = {}

    for var, meta in VARIAVEIS_YAML.categoricas.items():
        valores = meta.get("valores", {})

        for codigo, descricao in valores.items():
            col_entrada = f"{var}_{codigo}"

            if col_entrada in df.columns:
                col_saida = f"{var}_{descricao}"
                presentes.setdefault(var, []).append(
                    (col_entrada, col_saida)
                )

    return presentes

def agrega_categoricas_ano(df: pd.DataFrame, ano: str, nivel: str = "municipal") -> pd.DataFrame:

    col_ano = VARIAVEIS_YAML.coluna_ano
    col_peso = VARIAVEIS_YAML.coluna_peso

    if col_ano not in df.columns:
        raise ValueError(f"Coluna temporal '{col_ano}' não existe no dataframe.")

    anos_df = set(df[col_ano].unique())
    if len(anos_df) != 1 or str(list(anos_df)[0]) != str(ano):
        raise ValueError(f"DF contém ano inválido: {anos_df}")

    if nivel == "municipal":
        campos_group = VARIAVEIS_YAML.campos_padrao
    elif nivel == "estadual":
        campos_group = [VARIAVEIS_YAML.coluna_uf]
    elif nivel == "nacional":
        campos_group = []
    else:
        raise ValueError("nivel deve ser 'municipal', 'estadual' ou 'nacional'")

    if col_peso not in df.columns:
        raise ValueError(f"A coluna de peso '{col_peso}' não existe no DF.")

    resultados = []

    for var, codigos in VARIAVEIS_YAML.valores_categoricos.items():

        descricoes = VARIAVEIS_YAML.descricoes_categoricos[var]

        dfs_var = []

        for codigo in codigos:
            col_entrada = f"{var}_{codigo}"

            if col_entrada not in df.columns:
                continue

            descricao = descricoes[codigo]
            col_saida = f"{var}_{descricao}"

            df_aux = df.copy()
            df_aux["_VAL"] = df_aux[col_entrada].astype(float) * df_aux[col_peso]

            if campos_group:
                soma = df_aux.groupby(campos_group)["_VAL"].sum()
                total = df_aux.groupby(campos_group)[col_peso].sum()
            else:
                soma = pd.Series([df_aux["_VAL"].sum()])
                total = pd.Series([df_aux[col_peso].sum()])

            pct = (soma / total) * 100
            dfs_var.append(pct.rename(col_saida).to_frame())

        if dfs_var:
            resultados.append(pd.concat(dfs_var, axis=1))

    if not resultados:
        return pd.DataFrame()

    df_final = pd.concat(resultados, axis=1)

    if campos_group:
        df_final = df_final.reset_index()
    else:
        df_final.insert(0, "UF", "BRASIL")

    return df_final


def agrega_categoricas(
    leitores_por_ano: dict[str, callable],
    include_estadual: bool = True,
    include_nacional: bool = True,
):
    """
    Agrega variáveis categóricas no formato LONG,
    carregando um ano por vez para reduzir uso de memória.

    leitores_por_ano:
        dict ano -> função que retorna um df contendo apenas aquele ano
    include_estadual: se True, agrega também por estado
    include_nacional: se True, agrega também nacionalmente

    Retorna:
        {
            "municipal": df,
            "estadual": df ou None,
            "nacional": df ou None,
        }
    """

    ANO_COL = VARIAVEIS_YAML.coluna_ano

    result_mun = None
    result_est = None if include_estadual else None
    result_nat = None if include_nacional else None

    for ano, leitor in leitores_por_ano.items():

        df_cat = leitor()  # deve conter coluna ano = ano

        df_cat = df_cat[df_cat[ANO_COL].astype(str) == str(ano)]

        agg_mun_ano = agrega_categoricas_ano(df_cat, ano, nivel="municipal")
        agg_mun_ano[ANO_COL] = int(ano)

        if include_estadual:
            agg_est_ano = agrega_categoricas_ano(df_cat, ano, nivel="estadual")
            agg_est_ano[ANO_COL] = int(ano)

        if include_nacional:
            agg_nat_ano = agrega_categoricas_ano(df_cat, ano, nivel="nacional")
            agg_nat_ano[ANO_COL] = int(ano)

        # Primeira iteração
        if result_mun is None:
            result_mun = agg_mun_ano
            if include_estadual:
                result_est = agg_est_ano
            if include_nacional:
                result_nat = agg_nat_ano

        else:

            ANO_COL = VARIAVEIS_YAML.coluna_ano

            result_mun = pd.concat(
                [result_mun, agg_mun_ano],
                ignore_index=True
            )

            if include_estadual:
                result_est = pd.concat(
                    [result_est, agg_est_ano],
                    ignore_index=True
            )

            if include_nacional:
                result_nat = pd.concat([result_nat, agg_nat_ano], ignore_index=True)

        del df_cat, agg_mun_ano, agg_est_ano, agg_nat_ano
        gc.collect()

    retorno = {"municipal": result_mun}
    if include_estadual:
        retorno["estadual"] = result_est
    if include_nacional:
        retorno["nacional"] = result_nat

    return retorno

def merge_quantitativas_com_categoricas(
    df_quant_all: pd.DataFrame,
    cat_mun: pd.DataFrame,
    cat_est: pd.DataFrame,
    cat_nat: pd.DataFrame,
):
    """
    - Agrega quantitativas por município, estado e nacional.
    - Faz merge com as categóricas já agregadas.
    - Retorna os 3 níveis em um dict.
    """

    ANO_COL = VARIAVEIS_YAML.coluna_ano
    CAMPOS_PADRAO = VARIAVEIS_YAML.campos_padrao

    quant_mun = agrega_quantitativas(df_quant_all, nivel="municipal")
    quant_est = agrega_quantitativas(quant_mun, nivel="estadual")
    quant_nat = agrega_quantitativas(quant_est, nivel="nacional")

    # merge municipal
    chave_mun = CAMPOS_PADRAO + [ANO_COL]

    result_mun = quant_mun.merge(
        cat_mun,
        on=chave_mun,
        how="left",
    )

    # merge estadual

    chave_est = [VARIAVEIS_YAML.coluna_uf, ANO_COL]

    result_est = quant_est.merge(
        cat_est,
        on=chave_est,
        how="left",
    )

    # merge nacional
    chave_nat = [ANO_COL]

    result_nat = quant_nat.merge(
        cat_nat,
        on=chave_nat,
        how="left",
    )

    return {
        "municipal": result_mun,
        "estadual": result_est,
        "nacional": result_nat,
    }
