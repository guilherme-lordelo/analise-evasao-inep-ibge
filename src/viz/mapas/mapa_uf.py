import matplotlib.pyplot as plt
from viz.mapas.merge_spatial import merge_malha_evasao
from utils.config import load_config

def mapa_evasao_uf():
    config = load_config()
    coluna = config["evasao"]["coluna_padrao"]
    figsize = config["plot"]["figsize_uf"]
    cmap = config["plot"]["cmap"]

    gdf = merge_malha_evasao()

    if "SIGLA_UF" not in gdf.columns:
        raise ValueError("Coluna 'SIGLA_UF' não encontrada.")

    df_media = gdf.groupby("SIGLA_UF")[coluna].mean().reset_index()
    gdf_uf = gdf.dissolve(by="SIGLA_UF", as_index=False)
    gdf_uf = gdf_uf.merge(df_media, on="SIGLA_UF", how="left")

    plt.figure(figsize=figsize)
    gdf_uf.plot(
        column=coluna,
        cmap=cmap,
        legend=True,
        legend_kwds={"label": f"Evasão Média — {coluna}", "shrink": 0.6}
    )
    plt.title(f"Evasão por Estado — {coluna}")
    plt.axis("off")
    plt.show()
