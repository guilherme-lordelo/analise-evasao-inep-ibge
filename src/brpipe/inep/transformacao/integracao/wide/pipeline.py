import gc
import pandas as pd
from typing import Callable

from brpipe.utils.reduzir_colunas import reduzir_colunas

from .renomear_por_ano import renomear_com_ano
from .padronizacao import padronizar_categoricas
from .agregacao import agrega_categoricas


def fetch_categoricas(
	leitores_por_ano: dict[str, Callable[[], pd.DataFrame]],
	colunas_quantitativas: list[str],
	include_estadual: bool = True,
	include_nacional: bool = True,
):
	"""
	Recebe leitores prontos por ano e executa o pipeline WIDE de categóricas.
	"""

	def leitor_processado(ano: str):
		df = leitores_por_ano[ano]()

		df = reduzir_colunas(
			df,
			colunas_quantitativas,
			manter_peso=True,
			inplace=True,
		)

		df = renomear_com_ano(df, ano)
		df = padronizar_categoricas(df, ano)
		return df

	leitores = {
		ano: (lambda a=ano: leitor_processado(a))
		for ano in leitores_por_ano
	}

	return agrega_categoricas(
		leitores,
		include_estadual=include_estadual,
		include_nacional=include_nacional,
	)


def preparar_quantitativas(
	leitores_por_ano: dict[str, Callable[[], pd.DataFrame]],
	colunas_categoricas: list[str],
):
	"""
	Recebe leitores prontos por ano e executa o pipeline WIDE de quantitativas.
	"""

	dfs_quant = []

	for ano, leitor in leitores_por_ano.items():
		df_quant = leitor()

		df_quant = reduzir_colunas(
			df_quant,
			colunas_categoricas,
			inplace=True,
		)

		df_quant = renomear_com_ano(df_quant, ano)
		dfs_quant.append(df_quant)

	df_quant_all = pd.concat(dfs_quant, ignore_index=True)
	del dfs_quant
	gc.collect()

	return df_quant_all
