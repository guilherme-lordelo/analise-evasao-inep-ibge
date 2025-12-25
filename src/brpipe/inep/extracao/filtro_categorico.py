from brpipe.inep.config.loader import VARIAVEIS_YAML
import pandas as pd


def filtrar_variaveis_categoricas(
	df: pd.DataFrame,
) -> pd.DataFrame:
	"""
	Remove  linhas cujos valores foram excluídos
	por configuração (filtro_excluir).
	"""

	for coluna in VARIAVEIS_YAML.categoricas_original:
		if coluna not in df.columns:
			continue

		valores_permitidos = VARIAVEIS_YAML.valores_categoricos[coluna]

		antes = len(df)

		df = df[
			(df[coluna].isin(valores_permitidos)) |
			(df[coluna].isna())
		]

		depois = len(df)

		if antes != depois:
			print(
				f"Filtro categórico em '{coluna}': "
				f"{antes - depois} linhas removidas"
			)

	return df
