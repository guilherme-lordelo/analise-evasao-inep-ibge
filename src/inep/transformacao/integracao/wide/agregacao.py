import gc
from typing import Callable
import pandas as pd
from inep.config import (
    CAMPOS_PADRAO,
    COLUNA_UF,
    VARIAVEIS_QUANTITATIVAS,
    VALORES_CATEGORICOS,
    ANOS,
    COLUNA_PESO,
)

def agrega_quantitativas(df: pd.DataFrame, nivel: str = "municipal") -> pd.DataFrame:
    """
    Agrega quantitativas por município, estado ou nível nacional.

    nivel:
        - "municipal" : groupby por código e nome do município
        - "estadual"  : groupby pela UF (segundo campo de get_campos_municipio)
        - "nacional"  : soma total; retorna uma linha com a coluna UF="BRASIL"
    """

    # Define colunas quantitativas
    todas_quant_ano = {
        f"{var}_{ano}"
        for var in VARIAVEIS_QUANTITATIVAS
        for ano in ANOS
    }

    colunas_quant = sorted(c for c in df.columns if c in todas_quant_ano)

    if nivel == "municipal":
        colunas_groupby = CAMPOS_PADRAO

    elif nivel == "estadual":
        colunas_groupby = [CAMPOS_PADRAO[1]]

    elif nivel == "nacional":
        colunas_groupby = []

    else:
        raise ValueError("nivel deve ser 'municipal', 'estadual' ou 'nacional'")

    if colunas_groupby:
        agg = df.groupby(colunas_groupby, as_index=False)[colunas_quant].sum()
    else:
        soma = df[colunas_quant].sum().to_frame().T
        soma.insert(0, "UF", "BRASIL")
        agg = soma

    return agg


def agrega_categoricas_ano(df: pd.DataFrame, ano: str, nivel: str = "municipal") -> pd.DataFrame:
    """
    Agrega variáveis categóricas de um único ano no formato:
        VARIAVEL_VALOR_ANO
        VARIAVEL_OUTROS_ANO
    """

    # Cria dicionário de colunas
    presentes = {}

    for var, valores in VALORES_CATEGORICOS.items():
        lista_valores = list(valores) + ["OUTROS"]
        for valor in lista_valores:
            col = f"{var}_{valor}_{ano}"
            if col in df.columns:
                presentes[(var, valor)] = col

    # 
    lista_var = {}
    for (var, valor), col in presentes.items():
        lista_var.setdefault(var, []).append(col)

    # Ordenar cada variável pela lista de valores categóricos
    for var, colunas_var in lista_var.items():
        ordem = VALORES_CATEGORICOS[var]
        colunas_var.sort(
            key=lambda c: (
                ordem.index(c.split("_")[-2])
                if c.split("_")[-2] in ordem
                else len(ordem)  # OUTROS sempre por último
            )
        )

    if not lista_var:
        if nivel == "municipal":
            return df[CAMPOS_PADRAO].drop_duplicates()
        elif nivel == "estadual":
            return df[[CAMPOS_PADRAO[1]]].drop_duplicates()
        else:
            return pd.DataFrame({"UF": ["BRASIL"]})

    if nivel == "municipal":
        campos_group = CAMPOS_PADRAO
    elif nivel == "estadual":
        campos_group = [CAMPOS_PADRAO[1]]
    elif nivel == "nacional":
        campos_group = []
    else:
        raise ValueError("nivel deve ser 'municipal', 'estadual' ou 'nacional'")

    # Verifica se a coluna de peso existe
    col_peso = f"{COLUNA_PESO}_{ano}"
    if col_peso not in df.columns:
        raise ValueError(f"Peso '{col_peso}' não existe no dataframe para o ano {ano}.")

    df_aux = df[campos_group + [col_peso]].copy()

    resultados = []

    for var, colunas_var in lista_var.items():

        dfs_var = []

        for col in colunas_var:
            # Valor ponderado
            df_aux["_VAL"] = df[col].astype(float) * df[col_peso]

            if campos_group:
                df_sum = df_aux.groupby(campos_group)["_VAL"].sum()
                df_total = df_aux.groupby(campos_group)[col_peso].sum()
            else:
                df_sum = pd.Series([df_aux["_VAL"].sum()])
                df_total = pd.Series([df_aux[col_peso].sum()])

            # Percentual
            df_pct = (df_sum / df_total) * 100
            df_pct = df_pct.to_frame(col)

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
    leitores_por_ano: dict[str, Callable[[], pd.DataFrame]],
    include_estadual: bool = True,
    include_nacional: bool = True,
):
    """
    Agrega categóricas sem carregar todos os anos na memória.
    Cada ano é carregado somente quando usado.
    """

    result_mun = None
    result_est = None if include_estadual else None
    result_nat = None if include_nacional else None

    for ano, leitor in leitores_por_ano.items():

        df_cat = leitor()

        agg_mun_ano = agrega_categoricas_ano(df_cat, ano, nivel="municipal")
        agg_est_ano = agrega_categoricas_ano(df_cat, ano, nivel="estadual") if include_estadual else None
        agg_nat_ano = agrega_categoricas_ano(df_cat, ano, nivel="nacional") if include_nacional else None

        # Combina com resultados anteriores
        if result_mun is None:
            result_mun = agg_mun_ano
            if include_estadual: result_est = agg_est_ano
            if include_nacional: result_nat = agg_nat_ano
        else:
            # MUNICIPAL
            chave_municipal = CAMPOS_PADRAO
            result_mun = result_mun.merge(
                agg_mun_ano,
                on=chave_municipal,
                how="left"
            )

            # ESTADUAL
            if include_estadual:
                chave_estadual = ["SG_UF"]
                result_est = result_est.merge(
                    agg_est_ano,
                    on=chave_estadual,
                    how="left"
                )

            # NACIONAL
            if include_nacional:
                result_nat = pd.concat([result_nat, agg_nat_ano], ignore_index=True)

        del df_cat, agg_mun_ano, agg_est_ano, agg_nat_ano
        gc.collect()

    retorno = {"municipal": result_mun}
    if include_estadual: retorno["estadual"] = result_est
    if include_nacional: retorno["nacional"] = result_nat
    return retorno

def merge_quantitativas_com_categoricas(
    df_quant_all: pd.DataFrame,
    cat_mun: pd.DataFrame,
    cat_est: pd.DataFrame,
    cat_nat: pd.DataFrame,
):
    """
    Recebe o DF concatenado de quantitativas (todos os anos).
    Agrega municipal -> estadual -> nacional.
    Realiza merge com os resultados categóricos.
    """

    # Agregação quantitativa
    quant_mun = agrega_quantitativas(df_quant_all, nivel="municipal")
    quant_est = agrega_quantitativas(quant_mun, nivel="estadual")
    quant_nat = agrega_quantitativas(quant_est, nivel="nacional")

    # Merge com categóricas

    # MUNICIPAL
    result_mun = quant_mun.merge(
        cat_mun,
        on=CAMPOS_PADRAO,
        how="left",
    )

    # ESTADUAL
    result_est = quant_est.merge(
        cat_est,
        on=[COLUNA_UF],
        how="left",
    )

    # NACIONAL
    result_nat = quant_nat.merge(
        cat_nat,
        on=["UF"],
        how="left",
    )

    return {
        "municipal": result_mun,
        "estadual": result_est,
        "nacional": result_nat,
    }