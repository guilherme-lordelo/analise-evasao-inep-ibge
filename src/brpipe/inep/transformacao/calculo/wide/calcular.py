import re
import types
import pandas as pd
import numpy as np


IDENTIFIER_RE = re.compile(r"[A-Za-z_]\w*")


def _extrair_tokens(expr: str):
    return set(t for t in IDENTIFIER_RE.findall(expr) if not t.isdigit())


def _montar_contexto(df, tokens):
    contexto = {col: df[col] for col in df.columns}
    contexto["np"] = np

    for t in tokens:
        if t not in contexto:
            contexto[t] = pd.Series(np.nan, index=df.index)

    safe_context = {}
    for k, v in contexto.items():
        if isinstance(v, (types.ModuleType, types.FunctionType)):
            safe_context[k] = pd.Series(np.nan, index=df.index)
        else:
            safe_context[k] = v

    return safe_context


def _avaliar_regras(
    regras,
    limites_validacao,
    df,
    ano_base,
    ano_seguinte,
):
    """
    Retorna:
      - serie_codigos
      - serie_ok
    """
    if not regras:
        return None, None

    regras_proc = [
        r.replace("{p}", str(ano_base)).replace("{n}", str(ano_seguinte))
        for r in regras
    ]

    codigos = []
    oks = []

    for _, row in df.iterrows():
        contexto = {**row.to_dict(), **limites_validacao}
        bits = []

        for regra in regras_proc:
            try:
                ok = pd.eval(regra, local_dict=contexto)
                bits.append("1" if ok else "0")
            except Exception:
                bits.append("0")

        codigo = "".join(bits)
        codigos.append("BIN_" + codigo)
        oks.append(codigo != "" and all(b == "1" for b in bits))

    return (
        pd.Series(codigos, index=df.index),
        pd.Series(oks, index=df.index, dtype=bool),
    )


def _avaliar_expressao(
    expressao,
    df,
    ano_base,
    ano_seguinte,
):
    expr = (
        expressao
        .replace("{p}", str(ano_base))
        .replace("{n}", str(ano_seguinte))
    )

    tokens = _extrair_tokens(expr)
    tokens.discard("np")

    contexto = _montar_contexto(df, tokens)

    serie = pd.Series(np.nan, index=df.index, dtype="float64")

    try:
        resultado = eval(expr, {}, contexto)
        serie[:] = resultado
    except Exception as e:
        tipos_contexto = {k: type(contexto[k]).__name__ for k in tokens}
        faltantes = [t for t in tokens if t not in contexto]
        raise RuntimeError(
            f"Erro ao avaliar expressão:\n"
            f"  expr: {expr}\n"
            f"  exc: {e!r}\n"
            f"  tokens: {tokens}\n"
            f"  faltantes: {faltantes}\n"
            f"  tipos: {tipos_contexto}"
        ) from e

    return serie.round(4)


def calcular_formulas(
    df: pd.DataFrame,
    *,
    anos: list,
    formulas: dict,
    limites_validacao: dict,
) -> pd.DataFrame:

    for ano_base, ano_seguinte in zip(anos[:-1], anos[1:]):
        for nome_formula, config in formulas.items():

            regras = config.regras_validacao

            serie_codigos, serie_ok = _avaliar_regras(
                regras,
                limites_validacao,
                df,
                ano_base,
                ano_seguinte,
            )

            if serie_codigos is not None:
                df[f"{nome_formula.upper()}_REGRAS_{ano_base}_{ano_seguinte}"] = serie_codigos
                df[f"{nome_formula.upper()}_REGRAS_OK_{ano_base}_{ano_seguinte}"] = serie_ok
            else:
                serie_ok = pd.Series(True, index=df.index)

            valores = _avaliar_expressao(
                config.expressao,
                df,
                ano_base,
                ano_seguinte,
            )

            df[f"{nome_formula.upper()}_{ano_base}_{ano_seguinte}"] = (
                valores.where(serie_ok, np.nan)
            )

    return df
