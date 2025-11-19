import pandas as pd


def agrega_por_municipio(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(
        ["CO_MUNICIPIO", "SG_UF", "NO_MUNICIPIO"],
        as_index=False
    ).agg({
        "QT_ING_TOTAL": "sum",
        "QT_MAT_TOTAL": "sum",
        "QT_CONC_TOTAL": "sum"
    })


def agrega_com_sufixo(df: pd.DataFrame, ano: str) -> pd.DataFrame:
    agg = agrega_por_municipio(df)
    return agg.rename(columns={
        "QT_ING_TOTAL": f"QT_ING_TOTAL_{ano}",
        "QT_MAT_TOTAL": f"QT_MAT_TOTAL_{ano}",
        "QT_CONC_TOTAL": f"QT_CONC_TOTAL_{ano}",
    })
