from collections import defaultdict
from functools import reduce
import pandas as pd

from brpipe.ibge.carga.integracao import integrar_sheets_tabela
from brpipe.ibge.carga.persistencia import persistir_tabela_final
from brpipe.ibge.config.models import SheetsTransformados
from brpipe.ibge.transformacao.merge_tabela import (
	registrar_merges_tabela,
	executar_merges_lazy,
)
from brpipe.ibge.config import COLUNAS_BASE_IBGE


def carregar_ibge(
	sheets_transformados: list[SheetsTransformados],
) -> None:
	"""
	Camada LOAD do IBGE:
	- Processa cada tabela IBGE
	- Consolida tudo em um único DataFrame
	- Persiste apenas uma vez
	"""

	por_tabela: dict[str, list[SheetsTransformados]] = defaultdict(list)

	for item in sheets_transformados:
		por_tabela[item.tabela.tabela_id].append(item)

	df_global: pd.DataFrame | None = None

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

		if df_global is None:
			df_global = df_tabela
		else:
			df_global = df_global.merge(
				df_tabela,
				on=COLUNAS_BASE_IBGE,
				how="outer",
			)

	if df_global is not None and not df_global.empty:
		persistir_tabela_final(df=df_global)
