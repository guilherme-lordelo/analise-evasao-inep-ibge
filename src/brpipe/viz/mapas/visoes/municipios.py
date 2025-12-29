# src/brpipe/viz/mapas/visoes/municipios.py

from __future__ import annotations

import geopandas as gpd
from typing import Optional

from brpipe.viz.mapas.config import COLUNAS
from .base import VisaoTerritorial
from .filtros import filtrar_ano


class VisaoMunicipios(VisaoTerritorial):
    """
    Visão territorial para municípios.
    """

    def __init__(self, gdf: gpd.GeoDataFrame):
        super().__init__(gdf)

        cols = COLUNAS.territoriais.municipio
        self.coluna_chave = cols.malha
        self.coluna_uf = cols.uf

        self._uf: Optional[str] = None

    def set_uf(self, uf: Optional[str]) -> None:
        """Define filtro por UF."""
        self._uf = uf

    def _cache_key(self):
        return (self._ano, self._uf)

    def _build_view(self) -> gpd.GeoDataFrame:
        gdf = self._gdf_base

        if self.coluna_ano and self._ano is not None:
            
            col = self.coluna_ano

            if gdf[col].dtype == object:
                ano = str(self._ano)
            else:
                ano = self._ano

            gdf = filtrar_ano(df=gdf, coluna_ano=col, ano=ano)

        if self._uf is not None:
            gdf = gdf[gdf[self.coluna_uf] == self._uf]

        return gdf
