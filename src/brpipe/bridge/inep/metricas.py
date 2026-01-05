from brpipe.bridge.inep.tipos import ResultadoTipo, resolver_resultado_tipo
from brpipe.inep.config.formulas import FormulaConfig, FormulasConfig

class MetricaINEP:
    def __init__(
        self,
        nome: str,
        formula_cfg,
        resultado: ResultadoTipo,
    ):
        self.nome = nome
        self._cfg = formula_cfg
        self.resultado = resultado

    @property
    def lag(self) -> int:
        return 1

    def to_ratio(self, series):
        return self.resultado.to_ratio(series)

    def to_percent_0_100(self, series):
        return self.resultado.to_percent_0_100(series)

    def to_logit(self, series):
        return self.resultado.to_logit(series)


class FormulasParaMetricas:
    def __init__(self, cfg: FormulasConfig):
        self._cfg = cfg

    def listar_metricas(self) -> list[str]:
        _lista_formulas = list(self._cfg.formulas.keys())
        return [item.upper() for item in _lista_formulas]

    def resolver(self, nome: str) -> FormulaConfig:
        if nome not in self._cfg.formulas:
            raise KeyError(f"Métrica '{nome}' não definida no INEP")
        return self._cfg.formulas[nome]

    def resolver_com_formato(self, nome: str) -> MetricaINEP:
        cfg = self.resolver(nome)

        resultado = resolver_resultado_tipo(
            getattr(cfg, "formato", None)
        )

        return MetricaINEP(
            nome=nome,
            formula_cfg=cfg,
            resultado=resultado,
        )