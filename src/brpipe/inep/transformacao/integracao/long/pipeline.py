import gc
import pandas as pd
from typing import Callable

from brpipe.inep.transformacao.integracao.long.agregacao import agrega_categoricas
from brpipe.inep.transformacao.integracao.long.padronizacao import padronizar_categoricas
from brpipe.utils.reduzir_colunas import reduzir_colunas


def fetch_categoricas(
	leitores_por_ano: dict[str, Callable[[], pd.DataFrame]],
	colunas_quantitativas: list[str],
	include_estadual: bool = True,
	include_nacional: bool = True,
):
	"""
	Recebe leitores e executa o pipeline LONG de categóricas.
	"""

	def leitor_processado(ano: str):
		df = leitores_por_ano[ano]()

		df = reduzir_colunas(
			df,
			colunas_quantitativas,
			manter_peso=True,
			inplace=True,
		)

		df = padronizar_categoricas(df)
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
	colunas_quantitativas: list[str],
):
	"""
	Recebe leitores e executa o pipeline LONG de quantitativas.
	"""

	dfs_quant = []

	for ano, leitor in leitores_por_ano.items():
		df = leitor()

		df = reduzir_colunas(
			df,
			colunas_categoricas,
			inplace=True,
		)

		for var in colunas_quantitativas:
			if var in df.columns:
				df[var] = df[var].fillna(0.0).astype(float)

		dfs_quant.append(df)

	df_all = pd.concat(dfs_quant, ignore_index=True)
	del dfs_quant
	gc.collect()

	return df_all
