from typing import Dict, Iterable
from pandas import DataFrame


def integrar_sheets_tabela(
	dfs_sheets: Dict[str, DataFrame],
	colunas_base: Iterable[str],
) -> DataFrame | None:

	if not dfs_sheets:
		return None

	colunas_base = list(colunas_base)

	dfs = iter(dfs_sheets.values())

	df_final = next(dfs).set_index(colunas_base, drop=False)

	for df in dfs:
		df_idx = df.set_index(colunas_base, drop=False)
		df_final = df_final.join(
			df_idx.drop(columns=colunas_base),
			how="outer",
		)

	return df_final.reset_index(drop=True)
