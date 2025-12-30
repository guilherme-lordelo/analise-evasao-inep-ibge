import matplotlib.pyplot as plt
from .base import construir_mapa

def plot_mapa(
    gdf,
    coluna: str,
    figsize,
    cmap,
    legend_label,
    shrink=0.5,
    titulo=None,
):
    fig, ax = construir_mapa(
        gdf=gdf,
        coluna=coluna,
        figsize=figsize,
        cmap=cmap,
        legend_label=legend_label,
        shrink=shrink,
        titulo=titulo,
    )

    plt.show()
