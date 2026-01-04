import matplotlib.pyplot as plt

from brpipe.viz.charts.common import (
    VisualizadorVariavel,
    TipoChart,
    NormalizacaoPlot,
    persistir_chart,
)


def render_linha_temporal(
    df,
    variaveis,
    coluna_ano: str,
    plot_spec: NormalizacaoPlot,
    cfg,
):
    fig, ax = plt.subplots(figsize=cfg.plot.figsize)

    for nome_variavel in plot_spec.variaveis:

        var = variaveis.get_variavel(nome_variavel)
        viz = VisualizadorVariavel(var)

        df_plot = df[[coluna_ano, nome_variavel]].copy()

        if plot_spec.normalizacao == NormalizacaoPlot.RATIO:
            serie = viz.preparar_para_chart(
                df_plot[nome_variavel],
                TipoChart.LINHA_TEMPORAL,
            )
        else:
            serie = df_plot[nome_variavel]

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
