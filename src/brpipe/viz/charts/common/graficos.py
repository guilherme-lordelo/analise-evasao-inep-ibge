from brpipe.bridge.inep.tipos import ResultadoTipo
from brpipe.bridge.inep.variaveis import VariavelINEP
from brpipe.viz.charts.common.metadados import MetaVisual, meta_para_linha
from brpipe.viz.charts.common.enums import TipoChart

class VisualizadorVariavel:
    def __init__(self, variavel: VariavelINEP):
        self.var = variavel

    def preparar_para_chart(self, series, chart: TipoChart):
        if chart == TipoChart.LINHA_TEMPORAL:
            return self._para_linha_temporal(series)

        raise NotImplementedError(chart)

    def _para_linha_temporal(self, series):
        if self.var.resultado == ResultadoTipo.LOGIT:
            return self.var.to_ratio(series)

        return series

    def meta_para_chart(self, chart: TipoChart) -> MetaVisual:
        if chart == TipoChart.LINHA_TEMPORAL:
            return meta_para_linha(self.var)