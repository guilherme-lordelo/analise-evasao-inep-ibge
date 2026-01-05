import pandas as pd
from brpipe.viz.mapas.config import METRICAS

def normalizar_metrica_long(
	df: pd.DataFrame,
	*,
	coluna_territorio: str,
	coluna_uf: str | None,
	coluna_ano: str,
	anos: list[int] | None,
) -> pd.DataFrame:
	df = df.copy()

	if anos is not None:
		df = df[df[coluna_ano].isin(anos)]

	colunas = [coluna_territorio, coluna_ano]

	if coluna_uf is not None:
		colunas.insert(1, coluna_uf)

	return (
		df[colunas + METRICAS]
	)
