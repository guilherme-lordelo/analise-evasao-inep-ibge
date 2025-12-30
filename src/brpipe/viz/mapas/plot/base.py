import matplotlib.pyplot as plt

def construir_mapa(
    gdf,
    coluna: str,
    figsize,
    cmap,
    legend_label,
    shrink=0.5,
    titulo=None,
):
    fig, ax = plt.subplots(figsize=figsize)

    gdf.plot(
        column=coluna,
        cmap=cmap,
        legend=True,
        legend_kwds={
            "label": legend_label,
            "shrink": shrink,
        },
        ax=ax,
    )

    if titulo:
        ax.set_title(titulo)

    ax.axis("off")

    return fig, ax
