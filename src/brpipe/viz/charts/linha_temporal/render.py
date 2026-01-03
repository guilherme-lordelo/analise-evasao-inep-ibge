import matplotlib.pyplot as plt

from brpipe.viz.config.graficos import VisualizadorVariavel
from brpipe.viz.config.metadados import meta_para_linha
from brpipe.viz.config.tipos import TipoChart



def render_linha_temporal(
    df,
    variaveis,
    coluna_ano: str,
    nome_variavel: str,
    cfg,
):
    var = variaveis.get_variavel(nome_variavel)

    viz = VisualizadorVariavel(var)

    df_plot = df[[coluna_ano, nome_variavel]].copy()

    df_plot[nome_variavel] = viz.preparar_para_chart(
        df_plot[nome_variavel],
        TipoChart.LINHA_TEMPORAL,
    )

    meta = meta_para_linha(var)

    fig, ax = plt.subplots(figsize=cfg.plot.figsize)

    ax.plot(
        df_plot[coluna_ano],
        df_plot[nome_variavel],
        marker="o",
    )

    ax.set_xlabel("Ano")
    ax.set_ylabel(meta.y_label)

    if cfg.plot.mostrar_titulo:
        ax.set_title(nome_variavel)

    if cfg.plot.grid:
        ax.grid(True, alpha=0.3)

    fig.tight_layout()

    fig.savefig(
        f"{nome_variavel}.{cfg.formato_saida}",
        dpi=cfg.dpi,
    )

    plt.close(fig)
