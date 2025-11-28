import pandas as pd
import numpy as np
from utils.config import load_config

cfg = load_config("inep")

FORMULA_EVASAO = cfg["formula_evasao"]
FORMULA_TOTAL = cfg["formula_total_estudantes"]


def calcular_taxa_evasao(df: pd.DataFrame, ano_base: str, ano_seguinte: str) -> pd.DataFrame:
    # Todas as colunas reais
    colunas = {col: df[col] for col in df.columns}

    # Variáveis auxiliares permitidas
    base_context = {
        **colunas,
        "np": np
    }

    # Identifica registros válidos
    mask_validos = df[f"EVASAO_VALIDO_{ano_base}_{ano_seguinte}"]

    # Substitui placeholders {p} e {n}
    expr_evasao = FORMULA_EVASAO.format(p=ano_base, n=ano_seguinte)
    expr_total = FORMULA_TOTAL.format(p=ano_base, n=ano_seguinte)

    # Avalia a fórmula apenas nos válidos
    evasao = pd.Series(np.nan, index=df.index, dtype="float64")

    # Cria um contexto filtrado as colunas
    contexto_validos = {k: v[mask_validos] for k, v in colunas.items()}

    contexto_validos["np"] = np

    evasao.loc[mask_validos] = eval(expr_evasao, {}, contexto_validos)

    df[f"TAXA_EVASAO_{ano_base}_{ano_seguinte}"] = evasao.round(4)

    # Total de estudantes
    df[f"QT_ESTUDANTES_TOTAL_{ano_base}_{ano_seguinte}"] = eval(expr_total, {}, base_context)

    return df
