from brpipe.viz.charts.common import COLUNA_ANO, CONSUMIVEIS, LINHA_TEMPORAL, carregar_dataframe_por_plot
from brpipe.viz.charts.linha_temporal.render import render_linha_temporal

def executar_linha_temporal():
	for plot_spec in LINHA_TEMPORAL.plots:

		df = carregar_dataframe_por_plot(plot_spec)

		render_linha_temporal(
			df=df,
			consumiveis=CONSUMIVEIS,
			coluna_ano=COLUNA_ANO,
			plot_spec=plot_spec,
			cfg=LINHA_TEMPORAL,
		)
