import pandas as pd
from brpipe.bridge.inep.metricas import FormulasParaMetricas
from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.viz.charts.common import LINHA_TEMPORAL, carregar_dataframe_por_plot
from brpipe.viz.charts.common.consumiveis import ConsumiveisINEP
from brpipe.viz.charts.linha_temporal.render import render_linha_temporal

def executar_linha_temporal(
	variaveis: VariaveisINEP,
	metricas: FormulasParaMetricas,
	coluna_ano: str,
):
	for plot_spec in LINHA_TEMPORAL.plots:

		df = carregar_dataframe_por_plot(plot_spec, variaveis)

		consumiveis = ConsumiveisINEP(
			variaveis=variaveis,
			metricas=metricas,
		)

		render_linha_temporal(
			df=df,
			consumiveis=consumiveis,
			coluna_ano=coluna_ano,
			plot_spec=plot_spec,
			cfg=LINHA_TEMPORAL,
		)
