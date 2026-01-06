from pandas import Series
from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.bridge.common.wrappers import SerieFormatada
from brpipe.inep.config.variaveis import VariaveisConfig

from dataclasses import dataclass

@dataclass(frozen=True)
class VariavelINEP:
	nome: str
	resultado: "ResultadoTipo"
	dim_temporal: bool = True

	def aplicar_formato(self, series: Series) -> SerieFormatada:
		return self.resultado.apply(series)


class VariaveisINEP:
	def __init__(self, cfg: VariaveisConfig):
		self._cfg = cfg
		self._variaveis = self._build_variaveis()

	def _build_variaveis(self) -> dict[str, VariavelINEP]:
		variaveis: dict[str, VariavelINEP] = {}

		q = self._cfg.quantitativas

		if isinstance(q, dict):
			for nome, resultado in q.items():
				variaveis[nome] = VariavelINEP(nome, resultado)
		else:
			for nome in q:
				variaveis[nome] = VariavelINEP(nome, ResultadoTipo.COUNT)

		for nome_base, valores in self._cfg.valores_categoricos.items():
			for valor in valores:
				nome_coluna = f"{nome_base}_{valor}"

				variaveis[nome_coluna] = VariavelINEP(
					nome=nome_coluna,
					resultado=ResultadoTipo.PERCENT_0_100,
				)

		return variaveis

	@property
	def coluna_ano(self) -> str:
		return self._cfg.coluna_ano

	@property
	def territoriais(self) -> dict:
		return {
			"municipio": self._cfg.coluna_cod_municipio,
			"uf": self._cfg.coluna_uf,
		}

	def is_quantitativa(self, nome: str) -> bool:
		return nome in self._variaveis
	
	def is_categorica(self, nome: str) -> bool:
		return nome in self._cfg.categoricas
	
	def resolver(self, nome: str) -> VariavelINEP:
		try:
			return self._variaveis[nome]
		except KeyError:
			raise KeyError(f"Variável '{nome}' não encontrada")

	def get_meta_label(self, nome: str) -> str:
		var = self.resolver(nome)

		if var.resultado == ResultadoTipo.PERCENT_0_100:
			return f"{nome} (%)"
		if var.resultado == ResultadoTipo.PROPORTION:
			return f"{nome} (0–1)"
		return nome
