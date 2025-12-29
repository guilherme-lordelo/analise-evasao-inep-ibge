# src/brpipe/viz/mapas/visoes/filtros.py

import pandas as pd

def filtrar_ano(df: pd.DataFrame, ano: int | None, coluna_ano: str) -> pd.DataFrame:
    if ano is None:
        return df
    return df[df[coluna_ano] == ano]
