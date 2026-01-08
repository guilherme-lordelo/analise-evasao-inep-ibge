import pandas as pd
from brpipe.ibge.config.models import MergeLazyOp, SheetIBGEConfig, MergeColunasConfig



def _registrar_merge_com_snapshot(
	merge: MergeColunasConfig,
	valores: pd.DataFrame,
	peso_base: pd.Series | None,
) -> MergeLazyOp:

	valores = valores.apply(pd.to_numeric, errors="coerce")

	def _calc() -> pd.Series:
		if merge.metodo == "soma":
			return valores.sum(axis=1, skipna=True)

		if merge.metodo == "media_ponderada":
			if not merge.peso_merge:
				raise ValueError(
					f"Merge '{merge.destino}' exige peso_merge"
				)

			pesos = pd.Series(
				merge.peso_merge,
				index=valores.columns,
			)

			base = valores
			if peso_base is not None:
				base = valores.mul(peso_base, axis=0)

			num = base.mul(pesos, axis=1).sum(axis=1)
			den = base.sum(axis=1)

			return num / den.replace(0, pd.NA)

		raise ValueError(f"Método inválido: {merge.metodo}")

	return MergeLazyOp(
		destino=merge.destino,
		apply=_calc,
	)


def registrar_merges_tabela(
	df: pd.DataFrame,
	sheets_cfg: list[SheetIBGEConfig],
) -> list[MergeLazyOp]:

	ops: list[MergeLazyOp] = []

	for sheet in sheets_cfg:
		if not sheet.merges_colunas:
			continue

		for merge in sheet.merges_colunas:
			fontes = [c for c in merge.fontes if c in df.columns]
			if not fontes:
				continue

			valores = df[fontes].copy()

			peso_base = None
			if merge.coluna_peso and merge.coluna_peso in df.columns:
				peso_base = pd.to_numeric(
					df[merge.coluna_peso],
					errors="coerce",
				)

			op = _registrar_merge_com_snapshot(
				merge,
				valores,
				peso_base,
			)

			ops.append(op)

	return ops

def executar_merges_lazy(
	df: pd.DataFrame,
	ops: list[MergeLazyOp],
) -> pd.DataFrame:

	for op in ops:
		df[op.destino] = op.apply()

	return df
