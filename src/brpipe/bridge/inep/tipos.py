from enum import Enum, auto
from matplotlib.axes import Axes
from matplotlib.ticker import PercentFormatter, ScalarFormatter
from pandas import Series
from brpipe.bridge.inep.wrappers import SerieFormatada
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

	def _get_scale(self):
		if self is ResultadoTipo.LOGIT:
			return "logit"
		return None
	
	def _get_formatador(self):
		if self is ResultadoTipo.COUNT:
			return ScalarFormatter()

		if self in {
			ResultadoTipo.RATIO,
			ResultadoTipo.PROPORTION,
			ResultadoTipo.PERCENT_0_100,
		}:
			return PercentFormatter(xmax=100)

		return None
	
	def formatar(self, ax: Axes, orientacao: str = "y") -> None:
		formatador = self._get_formatador()
		if formatador is not None:
			if orientacao.lower() == "y":
				ax.yaxis.set_major_formatter(formatador)
			elif orientacao.lower() == "x":
				ax.xaxis.set_major_formatter(formatador)

		scale = self._get_scale()
		if scale is not None:
			ax.set_yscale(scale)
	
	def apply(self, series: Series) -> SerieFormatada:
		if self is not ResultadoTipo.COUNT:
			series = self.to_percent_0_100(series)
		return SerieFormatada(
			serie=series,
			resultado=self,
		)


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