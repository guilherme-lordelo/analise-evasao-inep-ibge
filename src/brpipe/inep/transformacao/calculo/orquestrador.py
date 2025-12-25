import gc
import pandas as pd

from brpipe.inep.config import (
    ANOS,
    VARIAVEIS_YAML,
    FORMULAS_CONFIG,
)

from brpipe.inep.transformacao.calculo.long.calcular import calcular_formulas as calcular_long
from brpipe.inep.transformacao.calculo.wide.calcular import calcular_formulas as calcular_wide

def _definir_estrategia(
    df: pd.DataFrame,
    formato: str = "long",
    col_ano: str | None = VARIAVEIS_YAML.coluna_ano,
    col_chave: str | None = None,
) -> pd.DataFrame:

    if formato == "wide":
        return calcular_wide(
            df,
            anos=list(ANOS),
            formulas=FORMULAS_CONFIG.formulas,
            limites_validacao=FORMULAS_CONFIG.limites_validacao,
        )

    if formato == "long":
        return calcular_long(
            df,
            anos=list(ANOS),
            formulas=FORMULAS_CONFIG.formulas,
            limites_validacao=FORMULAS_CONFIG.limites_validacao,
            campos_padrao=VARIAVEIS_YAML.campos_padrao,
            col_ano=col_ano,
            col_chave=col_chave,
        )

    raise ValueError("formato deve ser 'wide' ou 'long'")


def orquestrar_calculo(
    dfs: dict[str, pd.DataFrame],
    formato: str = "long"
) -> dict[str, pd.DataFrame]:

    resultados = {}
    for nivel, df in dfs.items():
        resultados[nivel] = _definir_estrategia(df, formato=formato)
        del df
        gc.collect()

    return resultados
