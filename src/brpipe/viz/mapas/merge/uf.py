from brpipe.viz.mapas.merge.municipios import merge_municipios_evasao
from brpipe.viz.mapas.config import COLUNAS

UF = COLUNAS.territoriais.municipio.uf

def merge_uf_evasao(coluna: str):
    gdf = merge_municipios_evasao()

    df_media = (
        gdf
        .groupby(UF)[coluna]
        .mean()
        .reset_index()
    )

    gdf_uf = gdf.dissolve(by=UF, as_index=False)

    return gdf_uf.merge(df_media, on=UF, how="left")
