from pandas import DataFrame

from brpipe.ibge.config import ARQUIVO_FINAL_IBGE
from brpipe.utils.paths import PROCESSED_IBGE
from brpipe.utils.io import write_csv


def persistir_tabela_final(
	df: DataFrame | None,
) -> None:
	"""
    Persiste o DataFrame final IBGE já integrada.
	"""
	if df is None or df.empty:
		print(f"Nenhum dado para persistir.")
		return

	path_out = PROCESSED_IBGE / ARQUIVO_FINAL_IBGE

	write_csv(df, path_out)
