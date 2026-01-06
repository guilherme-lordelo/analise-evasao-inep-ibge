from matplotlib import pyplot as plt
from brpipe.viz.charts.common.persistencia import persistir_chart


def finalizar_chart(
    fig,
    ax,
    *,
    titulo: str | None,
    grid: bool,
    persistir_args: dict,
):
    if titulo:
        ax.set_title(titulo)

    if grid:
        ax.grid(True, alpha=0.3)

    fig.tight_layout()

    persistir_chart(**persistir_args)

    plt.close(fig)
