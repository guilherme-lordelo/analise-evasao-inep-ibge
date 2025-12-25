import gc
import pandas as pd

from brpipe.inep.transformacao.calculo.long.calcular import calcular_formulas as calcular_long
from brpipe.inep.transformacao.calculo.wide.calcular import calcular_formulas as calcular_wide

from brpipe.inep.config.transformacao import INEPConfigTransformacao


def _definir_estrategia(
    df: pd.DataFrame,
    config: INEPConfigTransformacao,
    formato: str = "long",
    col_ano: str | None = None,
    col_chave: str | None = None,
) -> pd.DataFrame:

    if col_ano is None:
        col_ano = config.coluna_ano

    if formato == "wide":
        return calcular_wide(
            df,
            anos=config.anos,
            formulas=config.formulas,
            limites_validacao=config.limites_validacao,
        )

    if formato == "long":
        return calcular_long(
            df,
            anos=config.anos,
            formulas=config.formulas,
            limites_validacao=config.limites_validacao,
            campos_padrao=config.campos_padrao,
            col_ano=col_ano,
            col_chave=col_chave,
        )

    raise ValueError("formato deve ser 'wide' ou 'long'")


def orquestrar_calculo(
    dfs: dict[str, pd.DataFrame],
    config: INEPConfigTransformacao,
    formato: str = "long",
) -> dict[str, pd.DataFrame]:

    resultados = {}

    for nivel, df in dfs.items():
        resultados[nivel] = _definir_estrategia(
            df,
            config=config,
            formato=formato,
        )
        del df
        gc.collect()

    return resultados
