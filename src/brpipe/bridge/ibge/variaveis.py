from pandas import Series
from brpipe.bridge.common.tipos import ResultadoTipo
from brpipe.ibge.config.models import SheetIBGEConfig, TabelaIBGEConfig
from brpipe.viz.charts.common.consumiveis import Consumivel


class VariavelIBGE:
    def __init__(
        self,
        nome: str,
        resultado: ResultadoTipo,
        coluna: str,
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
		self._map = {}

		for tabela in tabelas_cfg.values():
			for sheet in tabela.sheets:
				self._registrar_sheet(sheet)

	def _registrar_sheet(self, sheet: SheetIBGEConfig):
		for col in sheet.colunas_especificas:
			print(col.tipo)
		for col in sheet.colunas_especificas:
			tipo = col.tipo

			self._map[col.nome.upper()] = VariavelIBGE(
				nome=col.nome,
				coluna=col.nome,
				resultado=tipo,
			)

		if sheet.merges_colunas:
			for merge in sheet.merges_colunas:
				tipo = col.tipo

				self._map[merge.destino.upper()] = VariavelIBGE(
					nome=merge.destino,
					coluna=merge.destino,
					resultado=tipo,
				)

		if sheet.transformacoes_colunas:
			for t in sheet.transformacoes_colunas:
				tipo = tipo = col.tipo

				self._map[t.destino.upper()] = VariavelIBGE(
					nome=t.destino,
					coluna=t.destino,
					resultado=tipo,
				)

	def resolver(self, nome: str) -> Consumivel:
		chave = nome.upper()
		if chave not in self._map:
			raise KeyError(f"Variável IBGE '{nome}' não definida")
		return self._map[chave]

	def listar(self) -> list[str]:
		return list(self._map.keys())