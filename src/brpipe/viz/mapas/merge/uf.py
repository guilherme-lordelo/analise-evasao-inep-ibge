from brpipe.viz.mapas.merge.municipios import merge_municipios_evasao
from brpipe.viz.mapas.config.config import colunas_municipio

uf = colunas_municipio()["uf"]

def merge_uf_evasao(coluna: str):
    gdf = merge_municipios_evasao()

    df_media = gdf.groupby(uf)[coluna].mean().reset_index()
    gdf_uf = gdf.dissolve(by=uf, as_index=False)

    return gdf_uf.merge(df_media, on=uf, how="left")