# src/brpipe/viz/mapas/visoes/uf.py

from __future__ import annotations

import geopandas as gpd

from brpipe.viz.mapas.config import COLUNAS
from .base import VisaoTerritorial
from .filtros import filtrar_ano


class VisaoUF(VisaoTerritorial):
    """
    Visão territorial para estados (UF).
    """

    def __init__(self, gdf: gpd.GeoDataFrame):
        super().__init__(gdf)

        cols = COLUNAS.territoriais.uf
        self.coluna_chave = cols.malha

    def _cache_key(self):
        return (self._ano,)

    def _build_view(self) -> gpd.GeoDataFrame:
        gdf = self._gdf_base.copy()

        if self.coluna_ano and self._ano is not None:
            
            col = self.coluna_ano

            gdf = filtrar_ano(df=gdf, coluna_ano=col, ano=self._ano)
        return gdf
