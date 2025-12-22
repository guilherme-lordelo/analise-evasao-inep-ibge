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


def agrega_categoricas_ano(df: pd.DataFrame, ano: str, nivel: str = "municipal") -> pd.DataFrame:
    """
    Versão LONG da agregação categórica.
    
    Espera DF com:
      - VARIAVEL_VALOR (ex.: TP_REDE_1)
      - COLUNA_ANO  (ex.: 'NU_ANO_CENSO')
      - COLUNA_PESO  (ex.: 'QT_MAT_TOTAL')
    """

    # Nome da coluna de ano
    col_ano = VARIAVEIS_YAML.coluna_ano
    if col_ano not in df.columns:
        raise ValueError(f"Coluna temporal '{col_ano}' não existe no dataframe.")

    anos_df = set(df[col_ano].unique())
    if len(anos_df) > 1:
        raise ValueError(f"DF contém múltiplos anos: {anos_df}. A função LONG aceita apenas um ano por vez.")

    if str(list(anos_df)[0]) != str(ano):
        raise ValueError(f"Parâmetro ano='{ano}', mas o DF contém ano {list(anos_df)[0]}.")

    presentes = {}

    for var, valores in VARIAVEIS_YAML.valores_categoricos.items():
        lista_valores = list(valores) + ["OUTROS"]
        for valor in lista_valores:
            col = f"{var}_{valor}"
            if col in df.columns:
                presentes.setdefault(var, []).append(col)

    if not presentes:
        if nivel == "municipal":
            return df[VARIAVEIS_YAML.campos_padrao].drop_duplicates()
        elif nivel == "estadual":
            return df[[VARIAVEIS_YAML.campos_padrao[1]]].drop_duplicates()
        else:
            return pd.DataFrame({"UF": ["BRASIL"]})

    if nivel == "municipal":
        campos_group = VARIAVEIS_YAML.campos_padrao
    elif nivel == "estadual":
        campos_group = [VARIAVEIS_YAML.campos_padrao[1]]
    elif nivel == "nacional":
        campos_group = []
    else:
        raise ValueError("nivel deve ser 'municipal', 'estadual' ou 'nacional'")

    # Verifica se a coluna de peso existe
    col_peso = VARIAVEIS_YAML.coluna_peso
    if col_peso not in df.columns:
        raise ValueError(f"A coluna de peso '{col_peso}' não existe no DF.")

    df_aux = df[campos_group + [col_peso]].copy()

    resultados = []

    for var, colunas_var in presentes.items():

        ordem = VARIAVEIS_YAML.valores_categoricos[var]
        colunas_var.sort(
            key=lambda c: (
                ordem.index(c.split("_")[-1])
                if c.split("_")[-1] in ordem
                else len(ordem)
            )
        )

        dfs_var = []

        for col in colunas_var:
            df_aux["_VAL"] = df[col].astype(float) * df[col_peso]

            if campos_group:
                df_sum = df_aux.groupby(campos_group)["_VAL"].sum()
                df_total = df_aux.groupby(campos_group)[col_peso].sum()
            else:
                df_sum = pd.Series([df_aux["_VAL"].sum()])
                df_total = pd.Series([df_aux[col_peso].sum()])

            df_pct = (df_sum / df_total) * 100

            col_saida = col

            df_pct = df_pct.to_frame(col_saida)
            dfs_var.append(df_pct)

        resultado_var = pd.concat(dfs_var, axis=1)
        resultados.append(resultado_var)

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
