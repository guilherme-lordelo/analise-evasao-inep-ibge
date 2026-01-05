import matplotlib.pyplot as plt
from pandas import DataFrame

from brpipe.viz.charts.common import (
    Visualizador,
    NormalizacaoPlot,
    TipoChart,
    persistir_chart,
)
from brpipe.viz.charts.common.consumiveis import ConsumiveisINEP
from brpipe.viz.charts.common.filtros import filtrar_ano_inicial
from brpipe.viz.charts.linha_temporal.config import LinhaTemporalConfig, LinhaTemporalPlotSpec


def render_scatter(
    df: DataFrame,
    consumiveis: ConsumiveisINEP,
    coluna_ano: str,
    plot_spec: LinhaTemporalPlotSpec,
    cfg: LinhaTemporalConfig,
):
    filtrar_ano_inicial(
        df,
        consumiveis=consumiveis,
        coluna_ano=coluna_ano,
        plot_spec=plot_spec,
    )

    item_x = consumiveis.get(plot_spec.eixo_x)
    item_y = consumiveis.get(plot_spec.eixo_y)

    viz_x = Visualizador(item_x)
    viz_y = Visualizador(item_y)

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

    ax.set_xlabel(item_x.nome)
    ax.set_ylabel(item_y.nome)

    if cfg.plot.mostrar_titulo:
        ax.set_title(plot_spec.nome)

    if cfg.plot.grid:
        ax.grid(True, alpha=0.3)

    fig.tight_layout()

    persistir_chart(
        fig=fig,
        tipo="scatter",
        nome=plot_spec.nome,
        formato=cfg.formato_saida,
        dpi=cfg.dpi,
    )

    plt.close(fig)
