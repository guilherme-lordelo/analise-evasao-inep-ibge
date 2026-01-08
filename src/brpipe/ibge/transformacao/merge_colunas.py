import pandas as pd
from pandas import DataFrame
from brpipe.ibge.config.models import MergeLazyOp, SheetIBGEConfig, MergeColunasConfig


def _registrar_merge(merge: MergeColunasConfig) -> MergeLazyOp:

	fontes = merge.fontes

	def _calc(df: DataFrame) -> pd.Series:
		valores = df[fontes].apply(pd.to_numeric, errors="coerce")

		if merge.metodo == "soma":
			return valores.sum(axis=1, skipna=True)

		if merge.metodo == "media_ponderada":
			if not merge.peso_merge:
				raise ValueError(f"Merge '{merge.destino}' exige peso_merge")

			pesos = pd.Series(merge.peso_merge, index=fontes)

			if merge.coluna_peso:
				base = pd.to_numeric(df[merge.coluna_peso], errors="coerce")
				valores = valores.mul(base, axis=0)

			numerador = valores.mul(pesos, axis=1).sum(axis=1)
			denominador = valores.sum(axis=1)

			return numerador / denominador.replace(0, pd.NA)

		raise ValueError(f"Método de merge não suportado: {merge.metodo}")

	return MergeLazyOp(
		destino=merge.destino,
		fontes=fontes,
		coluna_peso=merge.coluna_peso,
		apply=_calc,
		drop_cols=fontes,
	)

def registrar_merges_sheet(
	sheet_cfg: SheetIBGEConfig,
) -> list[MergeLazyOp]:

	if not sheet_cfg.merges_colunas:
		return []

	return [
		_registrar_merge(merge)
		for merge in sheet_cfg.merges_colunas
	]

def registrar_merges_tabela(
	sheets_cfg: list[SheetIBGEConfig],
) -> list[MergeLazyOp]:

	ops: list[MergeLazyOp] = []

	for sheet in sheets_cfg:
		ops.extend(registrar_merges_sheet(sheet))

	return ops

def executar_merges_lazy(
	df: DataFrame,
	ops: list[MergeLazyOp],
) -> DataFrame:

	for op in ops:
		colunas_faltantes = set(op.fontes)
		if op.coluna_peso:
			colunas_faltantes.add(op.coluna_peso)

		colunas_faltantes -= set(df.columns)

		if colunas_faltantes:
			raise ValueError(
				f"Merge '{op.destino}' não pode ser executado. "
				f"Colunas ausentes: {colunas_faltantes}"
			)

		df[op.destino] = op.apply(df)

		df = df.drop(columns=[
			c for c in op.drop_cols if c in df.columns
		])

	return df
