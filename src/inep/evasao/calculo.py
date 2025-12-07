import re
import types
import pandas as pd
import numpy as np
from inep.config import FORMULAS, LIMITES, COLUNA_PESO

IDENTIFIER_RE = re.compile(r"[A-Za-z_]\w*")


# ------------------------
# Utilidades internas
# ------------------------

def _extrair_tokens(expr: str):
    return set(t for t in IDENTIFIER_RE.findall(expr) if not t.isdigit())


def _is_indexable(obj):
    try:
        _ = obj[:1]
        return True
    except Exception:
        return False


def _montar_contexto(df, tokens, mask_validos):
    contexto_full = {col: df[col] for col in df.columns}
    contexto_full["np"] = np

    for t in tokens:
        if t not in contexto_full:
            contexto_full[t] = pd.Series(np.nan, index=df.index)

    safe_context = {}
    for k, v in contexto_full.items():
        if isinstance(v, types.ModuleType) or isinstance(v, types.FunctionType) or not _is_indexable(v):
            safe_context[k] = pd.Series(np.nan, index=df.index)
        else:
            safe_context[k] = v

    contexto_validos = {}
    for k, v in safe_context.items():
        if _is_indexable(v):
            contexto_validos[k] = v[mask_validos]
        else:
            contexto_validos[k] = pd.Series(np.nan, index=df[mask_validos].index)

    contexto_validos["np"] = np
    return contexto_full, contexto_validos


# ------------------------
# Avaliação de regras
# ------------------------

def _avaliar_regras(regras, df, ano_base, ano_seguinte):
    """
    Retorna:
      - serie_codigos: códigos binários com prefixo "BIN_"
      - serie_ok: boolean, True se todas as regras forem "1"
    """
    if not regras:
        return None, None  # sinaliza ausência de regras

    regras_proc = [
        r.replace("{p}", str(ano_base)).replace("{n}", str(ano_seguinte))
        for r in regras
    ]

    codigos = []
    oks = []

    for idx, row in df.iterrows():
        contexto = {**row.to_dict(), **LIMITES}
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
        pd.Series(oks, index=df.index, dtype=bool)
    )


# ------------------------
# Avaliação de fórmula
# ------------------------

def _avaliar_expressao(expressao, df, ano_base, ano_seguinte, mask_validos):
    expr = (
        expressao.replace("{p}", str(ano_base))
                 .replace("{n}", str(ano_seguinte))
    )

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


# ------------------------
# Função principal
# ------------------------

def calcular_formulas(df: pd.DataFrame, ano_base: str, ano_seguinte: str) -> pd.DataFrame:
    """
    Avalia as fórmulas do YAML, gera coluna de valor + coluna binária de regras.
    Também calcula a coluna de peso definida no YAML.
    """
    mask_validos = df.get(
        f"EVASAO_VALIDO_{ano_base}_{ano_seguinte}",
        pd.Series(True, index=df.index)
    )

    for nome_formula, config in FORMULAS.items():

        regras = config.get("validacao", [])

        # ==========================
        # 1) Avaliar regras
        # ==========================
        serie_codigos, serie_ok = _avaliar_regras(regras, df, ano_base, ano_seguinte)

        if serie_codigos is not None:
            df[f"{nome_formula.upper()}_REGRAS_{ano_base}_{ano_seguinte}"] = serie_codigos
            df[f"{nome_formula.upper()}_REGRAS_OK_{ano_base}_{ano_seguinte}"] = serie_ok
        else:
            serie_ok = pd.Series(True, index=df.index)  # sem regras → sempre OK

        # ==========================
        # 2) Calcular fórmula SOMENTE SE regras_ok == True
        # ==========================
        expressao = config["expressao"]
        serie_valores = _avaliar_expressao(
            expressao, df, ano_base, ano_seguinte, mask_validos
        )

        # Onde regras falham, força NaN
        serie_valores = serie_valores.where(serie_ok, np.nan)

        df[f"{nome_formula.upper()}_{ano_base}_{ano_seguinte}"] = serie_valores

    return df
