from pandas import DataFrame

from brpipe.utils.io import write_csv
from brpipe.utils.paths import arquivo_ibge_final


def persistir_tabela_final(
	df: DataFrame | None,
) -> None:
	"""
    Persiste o DataFrame final IBGE já integrada.
	"""
	if df is None or df.empty:
		print(f"Nenhum dado para persistir.")
		return

	write_csv(df, arquivo_ibge_final)
