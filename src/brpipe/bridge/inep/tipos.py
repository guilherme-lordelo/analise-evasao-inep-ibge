from enum import Enum, auto

from pandas import Series
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
	
	def apply(self, series) -> Series:
		if self is not ResultadoTipo.COUNT:
			return self.to_ratio(series)
		return series


def resolver_resultado_tipo(valor) -> ResultadoTipo:
	if valor is None:
		return ResultadoTipo.PROPORTION

	if isinstance(valor, ResultadoTipo):
		return valor

	if isinstance(valor, str):
		try:
			return ResultadoTipo[valor.upper()]
		except KeyError:
			raise ValueError(
				f"Formato '{valor}' inválido. "
				f"Suportados: {[e.name for e in ResultadoTipo]}"
			)

	raise TypeError(
		f"Formato deve ser str, ResultadoTipo ou None. Recebido: {type(valor)}"
	)