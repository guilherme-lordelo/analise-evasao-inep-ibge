from brpipe.bridge.inep.metricas import FormulasParaMetricas
from brpipe.bridge.inep.tipos import ResultadoTipo
from brpipe.bridge.inep.variaveis import VariaveisINEP


class ConsumiveisINEP:
    def __init__(
        self,
        variaveis: VariaveisINEP,
        metricas: FormulasParaMetricas | None = None,
    ):
        self._variaveis = variaveis
        self._metricas = metricas

    def get(self, nome: str):
        try:
            return self._variaveis.get_variavel(nome)
        except KeyError:
            pass

        if self._metricas:
            try:
                return self._metricas.resolver_com_formato(nome)
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
    