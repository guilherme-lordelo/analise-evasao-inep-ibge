import gc
import pandas as pd
from inep.config import COLUNA_ANO
from inep.transformacao.calculo.long.calcular import calcular_formulas as calcular_long
from inep.transformacao.calculo.wide.calcular import calcular_formulas as calcular_wide

def _definir_estrategia(
    df: pd.DataFrame,
    *,
    formato: str = "wide",
    col_ano: str | None = COLUNA_ANO,
    col_chave: str | None = None
) -> pd.DataFrame:
    """
    Aplica o cálculo das fórmulas definidas em FORMULAS no dataframe fornecido.

    - formato="wide": cálculo usando colunas na mesma linha
    - formato="long": cálculo usando linhas pareadas por ano

    Retorna o dataframe com novas colunas adicionadas.
    """

    if formato == "wide":
        return calcular_wide(df)

    if formato == "long":
        return calcular_long(
            df,
            col_ano=col_ano,
            col_chave=col_chave
        )

    raise ValueError("formato deve ser 'wide' ou 'long'")


def orquestrar_calculo(dfs: dict[str, "pd.DataFrame"]) -> dict[str, "pd.DataFrame"]:
    """
    Lê os arquivos gerados pela integração (municipal, estadual, nacional),
    aplica o cálculo das fórmulas e devolve os dataframes resultantes.
    """

    resultados = {}
    for nivel, df in dfs.items():
        resultados[nivel] = _definir_estrategia(df)

        del df
        gc.collect()

    return resultados
