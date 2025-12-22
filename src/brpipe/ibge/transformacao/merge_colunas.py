import pandas as pd
from pandas import DataFrame
from brpipe.ibge.config.tabelas import SheetIBGEConfig, MergeColunasConfig


def aplicar_merges_colunas(
	df: DataFrame,
	sheet_cfg: SheetIBGEConfig
) -> DataFrame:

	if not sheet_cfg.merges_colunas:
		return df

	for merge in sheet_cfg.merges_colunas:
		df = _aplicar_merge(df, merge)

	return df


def _aplicar_merge(df: DataFrame, merge: MergeColunasConfig) -> DataFrame:

	fontes_validas = [c for c in merge.fontes if c in df.columns]

	if not fontes_validas:
		return df

	valores = (
		df[fontes_validas]
		.apply(pd.to_numeric, errors="coerce")
	)

	if merge.metodo == "soma":
		df[merge.destino] = valores.sum(axis=1, skipna=True)

	elif merge.metodo == "media":
		df[merge.destino] = valores.mean(axis=1, skipna=True)

	# remove colunas fonte após o merge
	df = df.drop(columns=fontes_validas)

	return df
