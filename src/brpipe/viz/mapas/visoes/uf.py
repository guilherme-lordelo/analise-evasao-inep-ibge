# src/brpipe/viz/mapas/visoes/uf.py

from __future__ import annotations
import geopandas as gpd
from brpipe.viz.mapas.config import MALHA
from .base import VisaoTerritorial
from .filtros import filtrar_ano


class VisaoUF(VisaoTerritorial):
    """
    Visão territorial para estados (UF).
    """

    def __init__(self, gdf: gpd.GeoDataFrame):
        super().__init__(gdf)

        self.coluna_chave = MALHA.uf

    def _cache_key(self):
        return (self._ano,)

    def _build_view(self) -> gpd.GeoDataFrame:
        return self._aplicar_filtro_ano(self._gdf_base.copy())