from enum import Enum, auto

class TipoDado(Enum):
	COUNT = auto()
	PERCENT = auto()
	MEDIA = auto()
	RATIO = auto()
	PESO = auto()

	@classmethod
	def from_str(cls, valor: str, ctx: str) -> "TipoDado":
		if not isinstance(valor, str):
			raise TypeError(
				f"{ctx} Tipo de dado deve ser string. Recebido: {type(valor)}"
			)

		chave = valor.strip().upper()

		try:
			return cls[chave]
		except KeyError:
			raise ValueError(
				f"{ctx} Tipo de dado inválido: '{valor}'. "
				f"Suportados: {[e.name for e in cls]}"
            )


class TipoAgregacao(Enum):
	SOMA = auto()              # soma direta
	MEDIA_PONDERADA = auto()   # exige peso
	MEDIA_SIMPLES = auto()     # raramente correta
	RATIO_RECALCULADO = auto() # numerador / denominador
	NAO_AGREGAVEL = auto()     # quartil, mediana, índice
