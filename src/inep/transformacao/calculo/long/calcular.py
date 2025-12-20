import re
import types

import numpy as np
import pandas as pd

from inep.config import ANOS, VARIAVEIS_CONFIG, FORMULAS_CONFIG


IDENTIFIER_RE = re.compile(r"[A-Za-z_]\w*")

def _extrair_tokens(expr: str):
    return set(t for t in IDENTIFIER_RE.findall(expr) if not t.isdigit())


def _montar_contexto(df, tokens):
    """
    Cria o dicionário de contexto para eval()
    """
    contexto = {col: df[col] for col in df.columns}
    contexto["np"] = np

    for t in tokens:
        if t not in contexto:
            contexto[t] = pd.Series(np.nan, index=df.index)

    safe_context = {}
    for k, v in contexto.items():
        if isinstance(v, types.ModuleType) or isinstance(v, types.FunctionType):
            safe_context[k] = pd.Series(np.nan, index=df.index)
        else:
            safe_context[k] = v

    return safe_context


def _preparar_long_pareado(df, ano_base, ano_seguinte, col_ano, col_chave):
    """
    Retorna um dataframe com colunas _p e _n para anos base e seguinte.
    """
    df_p = (
        df[df[col_ano] == ano_base]
        .drop(columns=[col_ano])
        .add_suffix("_p")
    )

    df_n = (
        df[df[col_ano] == ano_seguinte]
        .drop(columns=[col_ano])
        .add_suffix("_n")
    )

    chave_p = f"{col_chave}_p"
    chave_n = f"{col_chave}_n"

    df_merge = df_p.merge(
        df_n,
        left_on=chave_p,
        right_on=chave_n,
        how="inner"
    )

    # manter chave limpa
    df_merge[col_chave] = df_merge[chave_p]

    return df_merge

def _avaliar_regras_long(
    regras,
    df,
    ano_base,
    ano_seguinte,
    col_ano,
    col_chave
):
    if not regras:
        return None

    df_calc = _preparar_long_pareado(
        df, ano_base, ano_seguinte, col_ano, col_chave
    )

    regras_proc = [
        r.replace("{p}", "p").replace("{n}", "n")
        for r in regras
    ]

    codigos = []
    oks = []

    for _, row in df_calc.iterrows():
        contexto = {**row.to_dict(), **FORMULAS_CONFIG.limites_validacao}
        bits = []

        for regra in regras_proc:
            try:
                ok = pd.eval(regra, local_dict=contexto)
                bits.append("1" if ok else "0")
            except Exception:
                bits.append("0")

        codigo = "".join(bits)
        codigos.append("BIN_" + codigo)
        oks.append(all(b == "1" for b in bits))

    return pd.DataFrame({
        col_chave: df_calc[col_chave],
        col_ano: ano_seguinte,
        "CODIGO": codigos,
        "OK": oks
    })


def _avaliar_expressao_long(
    expressao,
    df,
    ano_base,
    ano_seguinte,
    col_ano,
    col_chave
):
    df_calc = _preparar_long_pareado(
        df, ano_base, ano_seguinte, col_ano, col_chave
    )

    expr = (
        expressao
        .replace("{p}", "p")
        .replace("{n}", "n")
    )

    tokens = _extrair_tokens(expr)
    tokens.discard("np")

    contexto = _montar_contexto(df_calc, tokens)

    try:
        valores = eval(expr, {}, contexto)
    except Exception as e:
        raise RuntimeError(
            f"Erro ao avaliar expressão LONG:\n"
            f"  expr: {expr}\n"
            f"  exc: {e!r}"
        ) from e

    return pd.DataFrame({
        col_chave: df_calc[col_chave],
        col_ano: ano_seguinte,
        "VALOR": valores.round(4)
    })

def _resolver_coluna_chave(df: pd.DataFrame, col_chave: str | None) -> str:

    if col_chave in df.columns:
        return col_chave

    for c in VARIAVEIS_CONFIG.campos_padrao:
        if c in df.columns:
            return c

    if "UF_x" in df.columns:
        return "UF_x"

    raise ValueError("Nenhuma coluna de chave válida encontrada no dataframe")

def calcular_formulas(
    df: pd.DataFrame,
    *,
    col_ano: str,
    col_chave: str | None
) -> pd.DataFrame:

    if col_ano not in df.columns:
        raise ValueError(f"col_ano '{col_ano}' não encontrado no dataframe")

    col_chave = _resolver_coluna_chave(df, col_chave)

    for nome_formula, config in FORMULAS_CONFIG.formulas.items():

        nome_coluna = nome_formula.upper()

        if nome_coluna not in df.columns:
            df[nome_coluna] = np.nan

        regras = config.get("validacao", [])

        for ano_base, ano_seguinte in zip(ANOS[:-1], ANOS[1:]):

            df_regras = (
                _avaliar_regras_long(
                    regras,
                    df,
                    ano_base,
                    ano_seguinte,
                    col_ano,
                    col_chave
                )
                if regras else None
            )

            df_valores = _avaliar_expressao_long(
                config["expressao"],
                df,
                ano_base,
                ano_seguinte,
                col_ano,
                col_chave
            )

            if df_regras is not None:
                df_valores = df_valores.merge(
                    df_regras,
                    on=[col_chave, col_ano],
                    how="left"
                )

                df_valores["VALOR"] = df_valores["VALOR"].where(
                    df_valores["OK"], np.nan
                )

            mask = df[col_ano] == ano_seguinte

            df.loc[mask, nome_coluna] = (
                df.loc[mask]
                  .merge(
                      df_valores[[col_chave, col_ano, "VALOR"]],
                      on=[col_chave, col_ano],
                      how="left"
                  )["VALOR"]
                  .values
            )

    return df
