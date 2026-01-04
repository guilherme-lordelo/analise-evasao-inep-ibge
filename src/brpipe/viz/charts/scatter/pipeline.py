from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.viz.charts.common import (
	SCATTER,
	carregar_dataframe_por_plot,
)
from brpipe.viz.charts.scatter.render import render_scatter


def executar_scatter(
	variaveis: VariaveisINEP,
):
	for plot_spec in SCATTER.plots:

		df = carregar_dataframe_por_plot(plot_spec, variaveis)

		render_scatter(
			df=df,
			variaveis=variaveis,
			plot_spec=plot_spec,
			cfg=SCATTER,
		)
