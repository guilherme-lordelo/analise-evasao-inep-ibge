from pandas import DataFrame

from brpipe.utils.io import write_csv
from brpipe.utils.paths import ibge_municipio, ibge_estadual, ibge_nacional


def persistir_tabela_final(
	df: DataFrame | None,
	nivel: str,
) -> None:
	"""
    Persiste o DataFrame final IBGE já integrada.
	"""
	if df is None or df.empty:
		print(f"Nenhum dado para persistir.")
		return
	if nivel == "municipal":
		write_csv(df, ibge_municipio)
	elif nivel == "estadual":
		write_csv(df, ibge_estadual)
	elif nivel == "nacional":
		write_csv(df, ibge_nacional)
	else:
		print("Nível desconhecido. Deve ser 'municipal', 'estadual' ou 'nacional'")
