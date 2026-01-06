from brpipe.viz.charts.common.consumiveis import ConsumiveisINEP
from brpipe.viz.charts.common.persistencia import persistir_chart
from brpipe.viz.charts.common.plot_spec import PlotSpecBase
from brpipe.viz.charts.common.dataframe import carregar_dataframe_por_plot
from brpipe.viz.charts.common.graficos import Visualizador
from brpipe.viz.charts.common.metadados import MetaVisual, meta_para_linha
from brpipe.viz.charts.common.enums import NormalizacaoPlot, TipoChart
from brpipe.viz.charts.common.territorio import TerritoriosINEP
from brpipe.viz.charts.scatter.config import carregar_scatter
from ..linha_temporal.config import LinhaTemporalConfig, carregar_linha_temporal
from brpipe.bridge.inep import CONTEXTO

_variaveis=CONTEXTO.variaveis
_metricas=CONTEXTO.metricas
_territorios=TerritoriosINEP(_variaveis)

CONSUMIVEIS = ConsumiveisINEP(
    variaveis=_variaveis,
    metricas=_metricas,
)
COLUNA_ANO =_variaveis.coluna_ano

LINHA_TEMPORAL = carregar_linha_temporal(CONSUMIVEIS, _territorios)
SCATTER = carregar_scatter(CONSUMIVEIS, _territorios)

__all__ = [
    "CONSUMIVEIS",
    "COLUNA_ANO",
    "persistir_chart",
    "LINHA_TEMPORAL",
#    "SCATTER",
    "meta_para_linha",
    "LinhaTemporalConfig",
    "carregar_dataframe_por_plot",
    "TipoChart",
    "Visualizador",
    "MetaVisual",
    "PlotSpecBase",
    "NormalizacaoPlot",
]