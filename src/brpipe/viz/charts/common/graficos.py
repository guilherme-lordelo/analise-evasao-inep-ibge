from brpipe.bridge.inep.metricas import MetricaINEP
from brpipe.bridge.inep.variaveis import VariavelINEP
from brpipe.viz.charts.common.metadados import MetaVisual, meta_para_linha, meta_para_scatter
from brpipe.viz.charts.common.enums import TipoChart

class Visualizador:
    def __init__(self, item: VariavelINEP | MetricaINEP):
        self.item = item

    def preparar_para_chart(self, series, chart: TipoChart):
        if chart == TipoChart.LINHA_TEMPORAL:
            return series

        if chart == TipoChart.SCATTER:
            return series

        raise NotImplementedError(chart)

    def meta_para_chart(self, chart: TipoChart) -> MetaVisual:
        if chart == TipoChart.LINHA_TEMPORAL:
            return meta_para_linha(self.item)

        if chart == TipoChart.SCATTER:
            return meta_para_scatter(self.item)

        raise NotImplementedError(chart)
