import matplotlib.pyplot as plt
from pandas import DataFrame

from brpipe.viz.charts.common import (
    Visualizador,
    TipoChart,
)
from brpipe.viz.charts.common.consumiveis import ConsumiveisINEP
from brpipe.viz.charts.common.filtros import filtrar_ano_inicial
from brpipe.viz.charts.common.render_utils import finalizar_chart
from brpipe.viz.charts.scatter.config import ScatterConfig, ScatterPlotSpec


def render_scatter(
    df: DataFrame,
    consumiveis: ConsumiveisINEP,
    coluna_ano: str,
    plot_spec: ScatterPlotSpec,
    cfg: ScatterConfig,
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

    df_plot = df[[item_x.nome, item_y.nome]].copy()

    x = item_x.aplicar_formato(df_plot[item_x.nome])
    y = item_y.aplicar_formato(df_plot[item_y.nome])

    x = viz_x.preparar_para_chart(x, TipoChart.SCATTER)
    y = viz_y.preparar_para_chart(y, TipoChart.SCATTER)

    meta_x = viz_x.meta_para_chart(TipoChart.SCATTER)
    meta_y = viz_y.meta_para_chart(TipoChart.SCATTER)

    fig, ax = plt.subplots(figsize=cfg.plot.figsize)

    ax.scatter(x, y, alpha=0.7)

    ax.set_xlabel(meta_x.x_label)
    ax.set_ylabel(meta_y.y_label)


    finalizar_chart(
        fig,
        ax,
        titulo=plot_spec.nome if cfg.plot.mostrar_titulo else None,
        grid=cfg.plot.grid,
        persistir_args=dict(
            fig=fig,
            tipo="scatter",
            nome=plot_spec.nome,
            formato=cfg.formato_saida,
            dpi=cfg.dpi,
        ),
    )
