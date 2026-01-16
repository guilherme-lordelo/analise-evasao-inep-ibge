import matplotlib.pyplot as plt
from pandas import DataFrame

from brpipe.viz.charts.common import (
    Visualizador,
    TipoChart,
)
from brpipe.bridge.common.consumiveis import Consumiveis
from brpipe.viz.charts.common.render_utils import finalizar_chart
from brpipe.viz.charts.common.temporalidade import exigir_temporalidade
from brpipe.viz.charts.linha_temporal.config import LinhaTemporalConfig, LinhaTemporalPlotSpec


def render_linha_temporal(
    df: DataFrame,
    consumiveis: Consumiveis,
    coluna_ano: str,
    plot_spec: LinhaTemporalPlotSpec,
    cfg: LinhaTemporalConfig,
):
    fig, ax = plt.subplots(figsize=cfg.plot.figsize)
    tipo = None

    for nome in plot_spec.variaveis:
        item = consumiveis.get(nome)
        exigir_temporalidade(item, "Linha Temporal")
        coluna = item.nome

        viz = Visualizador(item)

        df_plot = df[[coluna_ano, coluna]].copy()

        serie_formatada = item.aplicar_formato(df_plot[coluna])
        serie = serie_formatada.serie
        tipo = serie_formatada.resultado

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
    if(tipo):
        tipo.formatar(ax)
    ax.set_xlabel("Ano")
    ax.legend()

    finalizar_chart(
        fig,
        ax,
        titulo=plot_spec.nome if cfg.plot.mostrar_titulo else None,
        grid=cfg.plot.grid,
        persistir_args=dict(
            fig=fig,
            tipo="linha_temporal",
            nome=plot_spec.nome,
            formato=cfg.formato_saida,
            dpi=cfg.dpi,
        ),
    )
