import pandas as pd
import gc

from brpipe.utils.paths import INEP_REDUZIDO
from brpipe.utils.io import read_csv
from brpipe.utils.reduzir_colunas import reduzir_colunas

from .renomear_por_ano import renomear_com_ano
from .padronizacao import padronizar_categoricas
from .agregacao import agrega_categoricas

from brpipe.inep.config import ARQUIVOS, VARIAVEIS_YAML


def fetch_categoricas(
	anos: list[str],
	include_estadual: bool = True,
	include_nacional: bool = True,
):
	"""
	Lê os anos, reduz para categóricas, renomeia com ano,
	agrega por município, estado e nacional.
	"""

	def leitor_ano(ano: str):
		df = read_csv(
			INEP_REDUZIDO
			/ f"{ARQUIVOS.extracao_prefixo_out}{ano}{ARQUIVOS.extracao_ext_out}"
		)
		df = reduzir_colunas(
			df,
			VARIAVEIS_YAML.quantitativas,
			manter_peso=True,
			inplace=True,
		)
		df = renomear_com_ano(df, ano)
		df = padronizar_categoricas(df, ano)
		return df

	leitores = {ano: (lambda a=ano: leitor_ano(a)) for ano in anos}

	return agrega_categoricas(
		leitores,
		include_estadual=include_estadual,
		include_nacional=include_nacional,
	)


def preparar_quantitativas(anos: list[str]):
	"""
	Lê os anos, reduz para quantitativas, renomeia com ano,
	e devolve o grande dataframe concatenado.
	"""

	dfs_quant = []

	for ano in anos:
		df_quant = read_csv(
			INEP_REDUZIDO
			/ f"{ARQUIVOS.extracao_prefixo_out}{ano}{ARQUIVOS.extracao_ext_out}"
		)
		df_quant = reduzir_colunas(
			df_quant,
			VARIAVEIS_YAML.categoricas,
			inplace=True,
		)
		df_quant = renomear_com_ano(df_quant, ano)

		dfs_quant.append(df_quant)

	df_quant_all = pd.concat(dfs_quant, ignore_index=True)
	del dfs_quant
	gc.collect()

	return df_quant_all
