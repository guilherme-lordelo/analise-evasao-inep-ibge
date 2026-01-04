import matplotlib.pyplot as plt
from pandas import DataFrame
import matplotlib.pyplot as plt
from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.viz.charts.common import (
    VisualizadorVariavel,
    TipoChart,
)
from brpipe.viz.charts.common.enums import NormalizacaoPlot
from brpipe.viz.charts.scatter.config import ScatterConfig, ScatterPlotSpec



def render_scatter(
    df: DataFrame,
    variaveis: VariaveisINEP,
    plot_spec: ScatterPlotSpec,
    cfg: ScatterConfig,
):
    var_x = variaveis.get_variavel(plot_spec.eixo_x)
    var_y = variaveis.get_variavel(plot_spec.eixo_y)

    viz_x = VisualizadorVariavel(var_x)
    viz_y = VisualizadorVariavel(var_y)

    df_plot = df[[plot_spec.eixo_x, plot_spec.eixo_y]].copy()

    if plot_spec.normalizacao == NormalizacaoPlot.RATIO:
        x = viz_x.preparar_para_chart(
            df_plot[plot_spec.eixo_x],
            TipoChart.SCATTER,
        )
        y = viz_y.preparar_para_chart(
            df_plot[plot_spec.eixo_y],
            TipoChart.SCATTER,
        )
    else:
        x = df_plot[plot_spec.eixo_x]
        y = df_plot[plot_spec.eixo_y]

    fig, ax = plt.subplots(figsize=cfg.plot.figsize)

    ax.scatter(x, y, alpha=0.7)

    ax.set_xlabel(var_x.nome)
    ax.set_ylabel(var_y.nome)


    if cfg.plot.mostrar_titulo:
        ax.set_title(plot_spec.nome)

    if cfg.plot.grid:
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(
        f"{plot_spec.nome}.{cfg.formato_saida}",
        dpi=cfg.dpi,
    )

    plt.close(fig)

