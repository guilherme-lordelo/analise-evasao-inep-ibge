from enum import Enum, auto

class TipoChart(Enum):
	LINHA_TEMPORAL = auto()
	BARRA = auto()
	LINHA = auto()
	HISTOGRAMA = auto()
	SCATTER = auto()

class NormalizacaoPlot(Enum):
	COUNT = auto()
	RATIO = auto()
