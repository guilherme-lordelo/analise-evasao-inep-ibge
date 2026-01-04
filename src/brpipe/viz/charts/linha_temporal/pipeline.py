import pandas as pd
from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.viz.charts.config import LINHA_TEMPORAL
from brpipe.viz.charts.config.linha_temporal import LinhaTemporalPlotSpec
from brpipe.viz.charts.linha_temporal.render import render_linha_temporal

from brpipe.utils.paths import (
	arquivo_nacional,
	arquivo_estadual,
	arquivo_municipal,
)
from brpipe.utils.io import read_csv


def carregar_dataframe_por_plot(
	plot_spec: LinhaTemporalPlotSpec,
	variaveis,
):
	if plot_spec.nivel == "nacional":
		df = read_csv(arquivo_nacional)

	elif plot_spec.nivel == "estadual":
		df = read_csv(arquivo_estadual)

		if plot_spec.territorio_chave == "ufs":
			col = variaveis.territoriais["uf"]
			df = df[df[col] == plot_spec.territorio_valor]

	elif plot_spec.nivel == "municipal":
		df = read_csv(arquivo_municipal)

		if plot_spec.territorio_chave == "municipios":
			col = variaveis.territoriais["municipio"]
			df = df[df[col] == plot_spec.territorio_valor]

	else:
		raise ValueError(f"Nível desconhecido: {plot_spec.nivel}")

	return df



def executar_linha_temporal(
	variaveis: VariaveisINEP,
	coluna_ano: str,
):
	for plot_spec in LINHA_TEMPORAL.plots:

		df = carregar_dataframe_por_plot(plot_spec, variaveis)

		#min_year = df[coluna_ano].min()
		#df = df[df[coluna_ano] > min_year]

		render_linha_temporal(
			df=df,
			variaveis=variaveis,
			coluna_ano=coluna_ano,
			plot_spec=plot_spec,
			cfg=LINHA_TEMPORAL,
		)
