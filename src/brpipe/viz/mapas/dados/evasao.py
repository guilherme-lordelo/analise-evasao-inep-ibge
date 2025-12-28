import pandas as pd

from brpipe.utils.paths import INEP_TRANSFORMACOES
from brpipe.viz.mapas.config.config import (
    arquivo_evasao,
    coluna_mapa,
    evasao_cfg,
    sep_evasao,
    formato_dados,
    colunas_municipio,
)


def _carregar_csv() -> pd.DataFrame:
    path = INEP_TRANSFORMACOES / arquivo_evasao()
    return pd.read_csv(path, sep=sep_evasao())

def _evasao_wide(df: pd.DataFrame) -> pd.DataFrame:
    cols = colunas_municipio()
    cfg = evasao_cfg()["wide"]

    return (
        df[
            [
                cols["tabela"],
                cols["uf"],
                cfg["coluna_valor"],
            ]
        ]
        .rename(columns={cfg["coluna_valor"]: coluna_mapa()})
    )



def _evasao_long(df: pd.DataFrame) -> pd.DataFrame:
    cfg = evasao_cfg()["long"]
    cols = colunas_municipio()

    df = df.copy()

    if "anos" in cfg:
        df = df[df[cfg["coluna_ano"]].isin(cfg["anos"])]

    return (
        df
        .groupby(
            [cols["tabela"], cols["uf"]],
            as_index=False
        )
        .agg({cfg["coluna_valor"]: cfg.get("agregacao", "mean")})
        .rename(columns={cfg["coluna_valor"]: coluna_mapa()})
    )


def carregar_evasao_municipios() -> pd.DataFrame:
    df = _carregar_csv()
    formato = formato_dados()

    if formato == "wide":
        return _evasao_wide(df)

    if formato == "long":
        return _evasao_long(df)

    raise ValueError(f"Formato de dados desconhecido: {formato}")
