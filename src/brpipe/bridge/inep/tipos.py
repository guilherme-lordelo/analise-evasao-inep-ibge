from enum import Enum, auto
from brpipe.utils.transformacoes import logit, inv_logit

class ResultadoTipo(Enum):
	COUNT = auto()
	RATIO = auto()
	PROPORTION = auto()
	LOGIT = auto()
	PERCENT_0_100 = auto()

	def to_ratio(self, series):
		if self == ResultadoTipo.COUNT:
			raise ValueError("COUNT não ser convertido para ratio")
		if self == ResultadoTipo.LOGIT:
			return inv_logit(series)
		if self == ResultadoTipo.PERCENT_0_100:
			return series / 100
		return series

	def to_percent_0_100(self, series):
		if self == ResultadoTipo.COUNT:
			raise ValueError("COUNT não ser convertido para percentual")
		if self == ResultadoTipo.LOGIT:
			return inv_logit(series) * 100
		if self in (ResultadoTipo.RATIO, ResultadoTipo.PROPORTION):
			return series * 100
		return series

	def to_logit(self, series):
		if self == ResultadoTipo.LOGIT:
			return series
		if self in (ResultadoTipo.RATIO, ResultadoTipo.PROPORTION):
			return logit(series)
		if self == ResultadoTipo.PERCENT_0_100:
			return logit(series / 100)
		raise ValueError("Conversão para logit não suportada")
