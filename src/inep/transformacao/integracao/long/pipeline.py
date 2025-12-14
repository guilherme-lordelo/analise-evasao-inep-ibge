import gc
import pandas as pd
from inep.config import EXTRACAO_EXT_OUT, EXTRACAO_PREFIXO_OUT, VARIAVEIS_CATEGORICAS, VARIAVEIS_QUANTITATIVAS
from inep.transformacao.integracao.long.agregacao import agrega_categoricas
from inep.transformacao.integracao.long.padronizacao import padronizar_categoricas
from utils.io import read_csv
from utils.paths import INEP_REDUZIDO
from utils.reduzir_colunas import reduzir_colunas


def fetch_categoricas(
    anos: list[str],
    include_estadual: bool = True,
    include_nacional: bool = True,
):
    """
    Lê cada ano individualmente, reduz para categóricas, padroniza,
    agrega por município, estado e nacional.
    """

    def leitor_ano(ano: str):
        df = read_csv(INEP_REDUZIDO / f"{EXTRACAO_PREFIXO_OUT}{ano}{EXTRACAO_EXT_OUT}")
        df = reduzir_colunas(df, VARIAVEIS_QUANTITATIVAS, manter_peso=True, inplace=True)
        df = padronizar_categoricas(df)

        return df

    leitores = {ano: (lambda a=ano: leitor_ano(a)) for ano in anos}

    return agrega_categoricas(
        leitores,
        include_estadual=include_estadual,
        include_nacional=include_nacional
    )

def preparar_quantitativas(anos: list[str]):
    """
    Lê os anos, reduz para quantitativas, e devolve o grande dataframe concatenado.
    """

    dfs_quant = []

    for ano in anos:
        df = read_csv(INEP_REDUZIDO / f"{EXTRACAO_PREFIXO_OUT}{ano}{EXTRACAO_EXT_OUT}")

        df = reduzir_colunas(df, VARIAVEIS_CATEGORICAS, inplace=True)

        for var in VARIAVEIS_QUANTITATIVAS:
            if var in df.columns:
                df[var] = df[var].fillna(0.0).astype(float)

        dfs_quant.append(df)

    df_all = pd.concat(dfs_quant, ignore_index=True)
    del dfs_quant; gc.collect()

    return df_all
