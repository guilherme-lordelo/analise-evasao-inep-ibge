import matplotlib.pyplot as plt
from pandas import DataFrame

from brpipe.viz.charts.common import (
    Visualizador,
    TipoChart,
    NormalizacaoPlot,
    persistir_chart,
)
from brpipe.viz.charts.common.consumiveis import ConsumiveisINEP
from brpipe.viz.charts.common.filtros import filtrar_ano_inicial
from brpipe.viz.charts.linha_temporal.config import LinhaTemporalConfig, LinhaTemporalPlotSpec


def render_linha_temporal(
    df: DataFrame,
    consumiveis: ConsumiveisINEP,
    coluna_ano: str,
    plot_spec: LinhaTemporalPlotSpec,
    cfg: LinhaTemporalConfig,
):
    fig, ax = plt.subplots(figsize=cfg.plot.figsize)

    for nome in plot_spec.variaveis:
        item = consumiveis.get(nome)
        coluna = item.nome

        viz = Visualizador(item)

        df_plot = df[[coluna_ano, coluna]].copy()

        serie = item.aplicar_formato(df_plot[coluna])

        serie = viz.preparar_para_chart(
            serie,
            TipoChart.LINHA_TEMPORAL,
        )

        meta = viz.meta_para_chart(TipoChart.LINHA_TEMPORAL)

        ax.plot(
            df_plot[coluna_ano],
            serie,
            marker="o",
            label=meta.y_label,
        )

    ax.set_xlabel("Ano")

    if cfg.plot.mostrar_titulo:
        ax.set_title(plot_spec.nome)

    if cfg.plot.grid:
        ax.grid(True, alpha=0.3)

    ax.legend()
    fig.tight_layout()

    persistir_chart(
        fig=fig,
        tipo="linha_temporal",
        nome=plot_spec.nome,
        formato=cfg.formato_saida,
        dpi=cfg.dpi,
    )

    plt.close(fig)
