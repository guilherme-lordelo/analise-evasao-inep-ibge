import re
import types
import pandas as pd
import numpy as np
from inep.config import FORMULAS, LIMITES

IDENTIFIER_RE = re.compile(r"[A-Za-z_]\w*")


# ------------------------
# Utilidades internas
# ------------------------

def _extrair_tokens(expr: str):
    """Extrai nomes de variáveis de uma expressão."""
    return set(t for t in IDENTIFIER_RE.findall(expr) if not t.isdigit())


def _is_indexable(obj):
    """Retorna True se o objeto aceita slicing (Series, numpy array, list)."""
    try:
        _ = obj[:1]
        return True
    except Exception:
        return False


def _montar_contexto(df, tokens, mask_validos):
    """
    Monta o contexto para eval: apenas variáveis indexáveis,
    sem módulos/funções, com fallback para Series NaN.
    """
    contexto_full = {col: df[col] for col in df.columns}
    contexto_full["np"] = np

    # Garantir que todos os tokens existam
    for t in tokens:
        if t not in contexto_full:
            contexto_full[t] = pd.Series(np.nan, index=df.index)

    # Converter módulos/funções ou não indexáveis para NaN
    safe_context = {}
    for k, v in contexto_full.items():
        if isinstance(v, types.ModuleType) or isinstance(v, types.FunctionType) or not _is_indexable(v):
            safe_context[k] = pd.Series(np.nan, index=df.index)
        else:
            safe_context[k] = v

    # Filtrar somente as linhas válidas
    contexto_validos = {}
    for k, v in safe_context.items():
        if _is_indexable(v):
            contexto_validos[k] = v[mask_validos]
        else:
            contexto_validos[k] = pd.Series(np.nan, index=df[mask_validos].index)

    contexto_validos["np"] = np
    return contexto_full, contexto_validos


# ------------------------
# Avaliação de expressões
# ------------------------

def _avaliar_expressao(expressao, df, ano_base, ano_seguinte, mask_validos):
    """
    Avalia uma expressão do YAML, substituindo {p} e {n}.
    """
    # Substituições
    expr = (
        expressao.replace("{p}", str(ano_base))
                 .replace("{n}", str(ano_seguinte))
    )

    # Tokens usados
    tokens = _extrair_tokens(expr)
    tokens.discard("np")

    contexto_full, contexto_validos = _montar_contexto(df, tokens, mask_validos)

    serie = pd.Series(np.nan, index=df.index, dtype="float64")

    try:
        resultado_validos = eval(expr, {}, contexto_validos)
        serie.loc[mask_validos] = resultado_validos
    except Exception as e:
        tipos_contexto = {k: type(contexto_full[k]).__name__ for k in tokens}
        faltantes = [t for t in tokens if t not in contexto_full]
        raise RuntimeError(
            f"Erro ao avaliar expressão:\n"
            f"  expr: {expr}\n"
            f"  exc: {e!r}\n"
            f"  tokens: {tokens}\n"
            f"  faltantes: {faltantes}\n"
            f"  tipos: {tipos_contexto}"
        ) from e

    return serie.round(4)


def _avaliar_regras(regras, df, ano_base, ano_seguinte):
    """
    Retorna uma Série onde cada elemento é uma string binária (ex: "1010"),
    representando o resultado das regras.
    """
    if not regras:
        return pd.Series([""] * len(df), index=df.index)

    # Substituir {p} e {n} nas regras
    regras_proc = [
        r.replace("{p}", str(ano_base)).replace("{n}", str(ano_seguinte))
        for r in regras
    ]

    codigos = []

    for idx, row in df.iterrows():
        contexto = {**row.to_dict(), **LIMITES}

        bits = []
        for regra in regras_proc:
            try:
                ok = pd.eval(regra, local_dict=contexto)
                bits.append("1" if ok else "0")
            except Exception:
                bits.append("0")  # erro → falha

        codigos.append("".join(bits))

    return pd.Series(codigos, index=df.index)


# ------------------------
# Função principal
# ------------------------

def calcular_formulas(df: pd.DataFrame, ano_base: str, ano_seguinte: str) -> pd.DataFrame:
    """
    Avalia as fórmulas do YAML, gera coluna de valor + coluna binária de regras.
    """
    mask_validos = df.get(
        f"EVASAO_VALIDO_{ano_base}_{ano_seguinte}",
        pd.Series(True, index=df.index)
    )

    for nome_formula, config in FORMULAS.items():

        # ==========================
        # Avaliar expressão
        # ==========================
        expressao = config["expressao"]
        serie_valores = _avaliar_expressao(
            expressao, df, ano_base, ano_seguinte, mask_validos
        )
        df[f"{nome_formula.upper()}_{ano_base}_{ano_seguinte}"] = serie_valores

        # ==========================
        # Avaliar regras
        # ==========================
        regras = config.get("validacao", [])
        serie_codigos = _avaliar_regras(regras, df, ano_base, ano_seguinte)
        df[f"{nome_formula.upper()}_REGRAS_{ano_base}_{ano_seguinte}"] = serie_codigos

    return df
