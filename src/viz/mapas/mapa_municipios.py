import matplotlib.pyplot as plt
from viz.mapas.merge_spatial import merge_malha_evasao
from utils.config import load_config

def mapa_evasao_municipios():
    config = load_config()
    coluna = config["evasao"]["coluna_padrao"]
    figsize = config["plot"]["figsize_municipios"]
    cmap = config["plot"]["cmap"]
    shrink = config["plot"]["legend_shrink"]

    gdf = merge_malha_evasao()

    plt.figure(figsize=figsize)
    gdf.plot(
        column=coluna,
        cmap=cmap,
        legend=True,
        legend_kwds={"label": f"Evasão ({coluna})", "shrink": shrink}
    )
    plt.title(f"Evasão por Município — {coluna}")
    plt.axis("off")
    plt.show()

def mapa_evasao_municipios_uf(sigla_uf: str):
    config = load_config()
    coluna = config["evasao"]["coluna_padrao"]
    figsize = config["plot"]["figsize_municipios"]
    cmap = config["plot"]["cmap"]
    shrink = config["plot"]["legend_shrink"]

    gdf = merge_malha_evasao()

    gdf = gdf[gdf["SIGLA_UF"] == sigla_uf.upper()]

    plt.figure(figsize=figsize)
    gdf.plot(
        column=coluna,
        cmap=cmap,
        legend=True,
        legend_kwds={"label": f"Evasão ({coluna}) — {sigla_uf}", "shrink": shrink}
    )
    plt.title(f"Evasão Municipal — {sigla_uf} — {coluna}")
    plt.axis("off")
    plt.show()
