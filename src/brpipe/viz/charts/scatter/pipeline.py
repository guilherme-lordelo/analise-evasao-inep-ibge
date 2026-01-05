from brpipe.bridge.inep.metricas import FormulasParaMetricas
from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.viz.charts.common.consumiveis import ConsumiveisINEP
from brpipe.viz.charts.common import (
    SCATTER,
    carregar_dataframe_por_plot,
)
from brpipe.viz.charts.scatter.render import render_scatter


def executar_scatter(
    variaveis: VariaveisINEP,
    metricas: FormulasParaMetricas,
	coluna_ano: str,
):
    
    consumiveis = ConsumiveisINEP(
        variaveis=variaveis,
        metricas=metricas,
    )

    for plot_spec in SCATTER.plots:
        df = carregar_dataframe_por_plot(plot_spec, variaveis)

        render_scatter(
            df=df,
            consumiveis=consumiveis,
			coluna_ano=coluna_ano,
            plot_spec=plot_spec,
            cfg=SCATTER,
        )
