from collections import defaultdict
import pandas as pd

from brpipe.ibge.transformacao.agregacao import executar_agregacoes
from brpipe.ibge.transformacao.integracao import integrar_sheets_tabela
from brpipe.ibge.config.models import SheetsTransformados
from brpipe.ibge.transformacao.merge_tabela import (
	registrar_merges_tabela,
	executar_merges_lazy,
)
from brpipe.ibge.config import COLUNAS_BASE_IBGE, TABELAS_IBGE


def carregar_ibge(
	sheets_transformados: list[SheetsTransformados],
) -> pd.DataFrame | None:
	"""
	Camada LOAD do IBGE:
	- Consolida todas as tabelas
	- Retorna o DataFrame municipal final
	"""

	por_tabela: dict[str, list[SheetsTransformados]] = defaultdict(list)

	for item in sheets_transformados:
		por_tabela[item.tabela.tabela_id].append(item)

	df_municipal: pd.DataFrame | None = None

	for tabela_id, items in por_tabela.items():
		dfs = {
			item.sheet.sheet_id or f"sheet_{i}": item.df
			for i, item in enumerate(items)
		}

		df_tabela = integrar_sheets_tabela(
			dfs_sheets=dfs,
			colunas_base=COLUNAS_BASE_IBGE,
		)

		if df_tabela is None or df_tabela.empty:
			continue

		merge_ops = registrar_merges_tabela(
			df=df_tabela,
			sheets_cfg=[item.sheet for item in items],
		)

		df_tabela = executar_merges_lazy(
			df=df_tabela,
			ops=merge_ops,
		)

		if df_municipal is None:
			df_municipal = df_tabela
		else:
			df_municipal = df_municipal.merge(
				df_tabela,
				on=COLUNAS_BASE_IBGE,
				how="outer",
			)

	executar_agregacoes(df_municipal, TABELAS_IBGE)
