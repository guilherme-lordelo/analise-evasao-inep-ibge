from pandas import Series
from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.ibge.config.models import SheetIBGEConfig, TabelaIBGEConfig
from brpipe.bridge.common.consumiveis import Consumivel


class VariavelIBGE:
	def __init__(
		self,
		nome: str,
		coluna: str,
		resultado: ResultadoTipo,
	):
		self.nome = nome.upper()
		self.coluna = coluna
		self.resultado = resultado

	def aplicar_formato(self, series: Series):
		return self.resultado.apply(series)


class VariaveisIBGE:
	def __init__(
		self,
		tabelas_cfg: dict[str, TabelaIBGEConfig],
	):
		self._map: dict[str, VariavelIBGE] = {}

		fontes_remover: set[str] = set()

		for tabela in tabelas_cfg.values():
			for sheet in tabela.sheets:
				self._registrar_colunas_sheet(sheet)
				self._registrar_merges_sheet(sheet, fontes_remover)

		for fonte in fontes_remover:
			self._map.pop(fonte.upper(), None)

	def _registrar_colunas_sheet(self, sheet: SheetIBGEConfig):
		for col in sheet.colunas_especificas:
			self._map[col.nome.upper()] = VariavelIBGE(
				nome=col.nome,
				coluna=col.nome,
				resultado=col.tipo_visualizacao,
			)

	def _registrar_merges_sheet(
		self,
		sheet: SheetIBGEConfig,
		fontes_remover: set[str],
	):
		if not sheet.merges_colunas:
			return

		for merge in sheet.merges_colunas:
			col = merge.coluna

			self._map[merge.destino.upper()] = VariavelIBGE(
				nome=merge.destino,
				coluna=merge.destino,
				resultado=col.tipo_visualizacao,
			)

			for fonte in merge.fontes:
				fontes_remover.add(fonte)

	def resolver(self, nome: str) -> Consumivel:
		chave = nome.upper()
		if chave not in self._map:
			raise KeyError(f"Variável IBGE '{nome}' não definida")
		return self._map[chave]

	def listar(self) -> list[str]:
		return list(self._map.keys())
