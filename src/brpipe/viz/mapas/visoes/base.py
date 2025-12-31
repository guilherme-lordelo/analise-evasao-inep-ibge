# src/brpipe/viz/mapas/visoes/base.py

from __future__ import annotations

import geopandas as gpd
from typing import Any, Dict, Optional, Tuple

from brpipe.viz.mapas.config import VARIAVEIS
from brpipe.viz.mapas.config import DADOS
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

        self.coluna_valor = DADOS.metrica_principal.coluna_mapa
        self.coluna_ano = (
            VARIAVEIS.coluna_ano
            if DADOS.metrica_principal.long
            else None
        )

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

    def to_plotly(self) -> Any:
        """
        Stub para integração futura com Plotly.
        """
        raise NotImplementedError("Integração Plotly ainda não implementada")

    def _cache_key(self) -> CacheKey:
        return (self._ano,)

    def _build_view(self) -> gpd.GeoDataFrame:
        gdf = self._gdf_base.copy()

        if self.coluna_ano and self._ano is not None:
            
            col = self.coluna_ano

            if gdf[col].dtype == object:
                ano = str(self._ano)
            else:
                ano = self._ano

            gdf = filtrar_ano(df=gdf, coluna_ano=col, ano=ano)

        return gdf