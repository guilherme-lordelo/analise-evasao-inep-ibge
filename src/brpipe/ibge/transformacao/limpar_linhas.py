import pandas as pd
import re

def is_codigo_municipio(value):
    """Retorna True para valores de 7 dígitos (ex: '4316477')."""
    if not isinstance(value, str):
        value = str(value)
    return bool(re.fullmatch(r"\d{7}", value.strip()))


def limpar(df: pd.DataFrame) -> pd.DataFrame:
	mask = df.iloc[:, 0].apply(is_codigo_municipio)
	df = df[mask].copy()
	df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
	return df
