from typing import Protocol
from pandas import Series
from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.bridge.common.wrappers import SerieFormatada

class Consumivel(Protocol):
    nome: str
    resultado: ResultadoTipo

    def aplicar_formato(self, series: Series) -> SerieFormatada:
        ...

class ConsumivelComTemporalidade(Consumivel, Protocol):
    dim_temporal: bool

class Container(Protocol):
    def resolver(self, nome: str) -> Consumivel:
        ...

class Consumiveis:
    def __init__(
        self,
        variaveis_inep: Container,
        metricas_inep: Container=None,
        variaveis_ibge: Container=None,
    ):
        self._variaveis_inep = variaveis_inep
        self._metricas_inep = metricas_inep
        self._variaveis_ibge = variaveis_ibge

    def get(self, nome: str) -> Consumivel:
        for container in (
            self._variaveis_inep,
            self._metricas_inep,
            self._variaveis_ibge,
        ):
            if not container:
                continue
            try:
                return container.resolver(nome)
            except KeyError:
                pass

        raise KeyError(f"'{nome}' não é um consumível conhecido")

    def get_meta_label(self, nome: str) -> str:
        obj = self.get(nome)

        if obj.resultado == ResultadoTipo.PERCENT_0_100:
            return f"{nome} (%)"
        if obj.resultado == ResultadoTipo.PROPORTION:
            return f"{nome} (0–1)"
        return nome
    