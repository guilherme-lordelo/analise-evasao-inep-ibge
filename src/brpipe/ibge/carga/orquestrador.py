from typing import List
from pandas import DataFrame
from brpipe.ibge.config import COLUNAS_BASE_IBGE
from brpipe.ibge.carga.integracao import integrar_sheets_tabela
from brpipe.ibge.carga.persistencia import persistir_tabela_final

def carregar_ibge(
	dfs: List[DataFrame],
) -> None:
	"""
	Camada LOAD do IBGE.

	- Recebe DataFrames já transformados
	- Integra sheets por tabela
	- Persiste o resultado final
	"""

	df_final = integrar_sheets_tabela(
		dfs_sheets={f"sheet_{i}": df for i, df in enumerate(dfs)},
		colunas_base=COLUNAS_BASE_IBGE,
	)

	persistir_tabela_final(
		df=df_final
	)
