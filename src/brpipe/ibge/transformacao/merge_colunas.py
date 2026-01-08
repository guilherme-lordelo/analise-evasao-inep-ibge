import pandas as pd
from pandas import DataFrame
from brpipe.ibge.config.models import SheetIBGEConfig, MergeColunasConfig


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

	fontes = [c for c in merge.fontes if c in df.columns]
	if not fontes:
		return df

	valores = df[fontes].apply(pd.to_numeric, errors="coerce")

	if merge.metodo == "soma":
		df[merge.destino] = valores.sum(axis=1, skipna=True)

	elif merge.metodo == "media_ponderada":
		if not merge.peso_merge:
			raise ValueError(f"Merge '{merge.destino}' exige peso_merge")

		if len(merge.peso_merge) != len(fontes):
			raise ValueError(
				f"Merge '{merge.destino}': peso_merge e fontes têm tamanhos diferentes"
			)

		pesos = pd.Series(merge.peso_merge, index=fontes)

		if merge.coluna_peso:
			base = pd.to_numeric(df[merge.coluna_peso], errors="coerce")
			valores_abs = valores.mul(base, axis=0)
		else:
			valores_abs = valores

		numerador = valores_abs.mul(pesos, axis=1).sum(axis=1)
		denominador = valores_abs.sum(axis=1)

		df[merge.destino] = numerador / denominador.replace(0, pd.NA)

	else:
		raise ValueError(f"Método de merge não suportado: {merge.metodo}")

	return df.drop(columns=fontes)
