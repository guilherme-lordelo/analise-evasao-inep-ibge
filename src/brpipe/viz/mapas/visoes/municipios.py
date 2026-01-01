# src/brpipe/viz/mapas/visoes/municipios.py

from __future__ import annotations
import geopandas as gpd
from typing import Optional
from brpipe.viz.mapas.config import VARIAVEIS, MALHA
from .base import VisaoTerritorial
from .filtros import filtrar_ano


class VisaoMunicipios(VisaoTerritorial):
    """
    Visão territorial para municípios.
    """

    def __init__(self, gdf: gpd.GeoDataFrame):
        super().__init__(gdf)

        self.coluna_chave = MALHA.municipio
        self.coluna_uf = VARIAVEIS.territoriais["uf"]

        self._uf: Optional[str] = None

    def set_uf(self, uf: Optional[str]) -> None:
        """Define filtro por UF."""
        self._uf = uf

    def _cache_key(self):
        return (self._ano, self._uf)

    def _build_view(self) -> gpd.GeoDataFrame:
        gdf = self._gdf_base.copy()

        if self.coluna_ano and self._ano is not None:
            
            col = self.coluna_ano

            gdf = filtrar_ano(df=gdf, coluna_ano=col, ano=self._ano)

        if self._uf is not None:
            gdf = gdf[gdf[self.coluna_uf] == self._uf]

        return gdf
