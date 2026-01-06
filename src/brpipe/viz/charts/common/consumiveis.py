from typing import Protocol
from pandas import Series
from brpipe.bridge.inep.metricas import FormulasParaMetricas
from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.bridge.inep.variaveis import VariaveisINEP
from brpipe.bridge.common.wrappers import SerieFormatada

class Consumivel(Protocol):
    nome: str
    resultado: ResultadoTipo

    def aplicar_formato(self, series: Series) -> SerieFormatada:
        ...

class Consumiveis:
    def __init__(
        self,
        variaveis: VariaveisINEP,
        metricas: FormulasParaMetricas | None = None,
    ):
        self._variaveis = variaveis
        self._metricas = metricas

    def get(self, nome: str) -> Consumivel:
        try:
            return self._variaveis.get_variavel(nome)
        except KeyError:
            pass

        if self._metricas:
            try:
                return self._metricas.resolver(nome)
            except KeyError:
                pass

        raise KeyError(
            f"'{nome}' não é uma variável nem uma métrica configurada"
        )

    def get_meta_label(self, nome: str) -> str:
        obj = self.get(nome)

        if obj.resultado == ResultadoTipo.PERCENT_0_100:
            return f"{nome} (%)"
        if obj.resultado == ResultadoTipo.PROPORTION:
            return f"{nome} (0–1)"
        return nome
    