import pandas as pd
from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.viz.charts.common import LINHA_TEMPORAL, carregar_dataframe_por_plot
from brpipe.viz.charts.linha_temporal.render import render_linha_temporal

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
