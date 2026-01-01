import matplotlib.pyplot as plt

def _plotar_se_nao_vazio(gdf, **kwargs):
    if gdf.empty:
        return
    gdf.plot(**kwargs)


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

    ax.set_aspect("equal")

    _plotar_se_nao_vazio(
        gdf[gdf["sem_inep"]],
        ax=ax,
        color="#9e9e9e",
        edgecolor="#636363",
        linewidth=0.3,
        label="Fora do INEP",
    )

    _plotar_se_nao_vazio(
        gdf[gdf["sem_metrica"]],
        ax=ax,
        color="#c6dbef",
        edgecolor="#6baed6",
        linewidth=0.3,
        label="Sem métrica",
    )

    _plotar_se_nao_vazio(
        gdf[~gdf["sem_inep"] & ~gdf["sem_metrica"]],
        column=coluna,
        cmap=cmap,
        legend=True,
        legend_kwds={
            "label": legend_label,
            "shrink": shrink,
        },
        ax=ax,
        edgecolor="white",
        linewidth=0.2,
    )

    if titulo:
        ax.set_title(titulo)

    ax.axis("off")
    ax.set_facecolor("white")

    return fig, ax
