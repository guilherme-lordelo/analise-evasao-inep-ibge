import pandas as pd

def aplicar_schema_ibge(
	df: pd.DataFrame,
	colunas_base: list[str],
	colunas_tabela: list[str]
) -> pd.DataFrame:

	colunas_finais = colunas_base + colunas_tabela
	df = df.iloc[:, :len(colunas_finais)]
	df.columns = colunas_finais
	return df
