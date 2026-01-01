# src/brpipe/viz/mapas/visoes/base.py

from __future__ import annotations

import geopandas as gpd
from typing import Any, Dict, Optional, Tuple

from brpipe.viz.mapas.config import VARIAVEIS
from .filtros import filtrar_ano


CacheKey = Tuple[Any, ...]


class VisaoTerritorial:
    """
    Classe base para visões territoriais (UF, município, etc).

    - Mantém estado de filtros
    - Fornece GeoDataFrames prontos para plotagem
    - Cache em memória por combinação de filtros
    """

    def __init__(self, gdf: gpd.GeoDataFrame) -> None:
        self._gdf_base = gdf
        self._cache: Dict[CacheKey, gpd.GeoDataFrame] = {}

        self._ano: Optional[int] = None

        self.coluna_ano = VARIAVEIS.coluna_ano

    def set_ano(self, ano: Optional[int]) -> None:
        """Define o ano ativo da visão."""
        self._ano = ano

    def get_view(self) -> gpd.GeoDataFrame:
        """
        Retorna a visão atual, aplicando filtros e cache.
        """
        key = self._cache_key()

        if key not in self._cache:
            self._cache[key] = self._build_view()

        return self._cache[key]

    def clear_cache(self) -> None:
        self._cache.clear()

    def _cache_key(self) -> CacheKey:
        return (self._ano,)

    def _aplicar_filtro_ano(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        if not self.coluna_ano or self._ano is None:
            return gdf

        col = self.coluna_ano
        ano = str(self._ano) if gdf[col].dtype == object else self._ano

        mask = (gdf[col] == ano) | (gdf[col].isna())
        return gdf[mask]

    def _build_view(self) -> gpd.GeoDataFrame:
        gdf = self._gdf_base.copy()
        return self._aplicar_filtro_ano(gdf)