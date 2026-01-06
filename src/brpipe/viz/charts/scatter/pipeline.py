from brpipe.viz.charts.common import (
    COLUNA_ANO,
    CONSUMIVEIS,
    SCATTER,
    carregar_dataframe_por_plot,
)
from brpipe.viz.charts.scatter.render import render_scatter


def executar_scatter():
    for plot_spec in SCATTER.plots:

        df = carregar_dataframe_por_plot(plot_spec)

        render_scatter(
			df=df,
			consumiveis=CONSUMIVEIS,
			coluna_ano=COLUNA_ANO,
			plot_spec=plot_spec,
            cfg=SCATTER,
        )
