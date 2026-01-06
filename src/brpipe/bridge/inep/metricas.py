from pandas import Series
from brpipe.bridge.common.tipos import ResultadoTipo, resolver_resultado_tipo
from brpipe.bridge.common.wrappers import SerieFormatada
from brpipe.inep.config.formulas import FormulasConfig

class MetricaINEP:
    def __init__(
        self,
        nome: str,
        formula_cfg,
        resultado: ResultadoTipo,
    ):
        self.nome = nome.upper()
        self._cfg = formula_cfg
        self.resultado = resultado
        self.dim_temporal: bool = True

    @property
    def lag(self) -> int:
        return 1

    def aplicar_formato(self, series: Series) -> SerieFormatada:
        return self.resultado.apply(series)


class FormulasParaMetricas:
    def __init__(self, cfg: FormulasConfig):
        self._cfg = cfg

        self._index_ci = {
            nome.upper(): nome
            for nome in cfg.formulas.keys()
        }

    def listar_metricas(self) -> list[str]:
        return list(self._index_ci.keys())

    def resolver(self, nome: str) -> MetricaINEP:
        chave = nome.upper()

        if chave not in self._index_ci:
            raise KeyError(f"Métrica '{nome}' não definida no INEP")

        nome_real = self._index_ci[chave]
        cfg = self._cfg.formulas[nome_real]

        resultado = resolver_resultado_tipo(
            cfg.formato or ResultadoTipo.PROPORTION
        )

        return MetricaINEP(
            nome=nome_real,
            formula_cfg=cfg,
            resultado=resultado,
        )
